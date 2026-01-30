import cv2
import subprocess
import logging
from ultralytics import YOLO
import os
from pathlib import Path

# --- Configuration ---
MODEL_PATH = "yoloModels/rtdetr-x.pt"
INPUT_URL = "rtmp://localhost/live/livestream"
OUTPUT_URL = "rtmp://localhost/live/output"

BASE_DIR = Path(__file__).resolve().parent
HLS_DIR = BASE_DIR / "srs-www" / "live"
HLS_DIR.mkdir(parents=True, exist_ok=True)
HLS_OUTPUT = str(HLS_DIR / "output.m3u8")
print("HLS_OUTPUT =", HLS_OUTPUT)
# --- End Configuration ---


def main():
    """
    Captures a video stream, processes it with a YOLO model, and streams the
    annotated video to an RTMP server using FFmpeg.
    """
    logging.basicConfig(level=logging.INFO)

    # Before running, ensure you have an RTMP server running.
    # e.g., with Docker: docker run -d -p 1935:1935 --name nginx-rtmp nginx-rtmp

    # Load the YOLO model
    try:
        model = YOLO(MODEL_PATH)
        logging.info(f"Successfully loaded model from {MODEL_PATH}")
    except Exception as e:
        logging.error(f"Failed to load YOLO model: {e}")
        return

    # Use OpenCV to capture the input stream to determine its properties
    cap = cv2.VideoCapture(INPUT_URL)
    if not cap.isOpened():
        logging.error(f"Error: Could not open input stream at {INPUT_URL}")
        return

    # Get video properties from the source
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()  # Release the capture object, ultralytics will handle it

    logging.info(f"Input stream properties: {width}x{height} @ {fps} FPS")

    # --- FFmpeg Subprocess for Streaming ---
    # This command sets up FFmpeg to receive raw video frames (in BGR
    # pixel format, which is OpenCV's default) from its stdin, encode
    # them using the libx264 codec, and stream them in FLV format to the
    # output RTMP URL.
    # ffmpeg_command ffmpeg_command = [

    OUTPUT_FPS = 5
    GOP = OUTPUT_FPS * 2  # 2 Sekunden

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "warning",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "bgr24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(OUTPUT_FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-tune",
        "zerolatency",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "baseline",
        "-level",
        "3.1",
        "-g",
        str(GOP),
        "-keyint_min",
        str(GOP),
        "-sc_threshold",
        "0",
        "-f",
        "hls",
        "-hls_time",
        "2",
        "-hls_list_size",
        "6",
        "-hls_flags",
        "delete_segments+append_list+omit_endlist",
        "-hls_allow_cache",
        "0",
        "-hls_segment_filename",
        str(HLS_DIR / "output%d.ts"),
        str(HLS_OUTPUT),
    ]

    # ffmpeg= [
    #     "ffmpeg",
    #     "-y",
    #     "-f",
    #     "rawvideo",
    #     "-vcodec",
    #     "rawvideo",
    #     "-pix_fmt",
    #     "bgr24",
    #     "-s",
    #     f"{width}x{height}",
    #     "-r",
    #     str(fps),
    #     "-i",
    #     "-",
    #     "-c:v",
    #     "libx264",
    #     "-pix_fmt",
    #     "yuv420p",
    #     "-preset",
    #     "medium",
    #     "-tune",
    #     "zerolatency",
    #     "-profile:v",
    #     "baseline",
    #     # RTMP Output
    #     "-f",
    #     "flv",
    #     OUTPUT_URL,
    #     # HLS Output
    #     "-c:v",
    #     "libx264",
    #     "-f",
    #     "hls",
    #     "-hls_time",
    #     "2",
    #     "-hls_list_size",
    #     "5",
    #     "-hls_flags",
    #     "delete_segments",
    #     "/usr/local/srs/objs/nginx/html/live/output.m3u8",
    # ]

    # Start the FFmpeg subprocess
    try:
        process = subprocess.Popen(
            ffmpeg_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if process.stdin is None:
            logging.error("Failed to open stdin for FFmpeg subprocess.")
            return

        logging.info("Started FFmpeg subprocess for streaming.")
    except FileNotFoundError:
        logging.error(
            "FFmpeg not found. Please ensure it is installed and in your PATH."
        )
        return
    except Exception as e:
        logging.error(f"Failed to start FFmpeg subprocess: {e}")
        return

    try:
        # Process the stream with the YOLO model
        results = model.track(source=INPUT_URL, stream=True, tracker="bytetrack.yaml")

        for result in results:
            # Get the annotated frame
            annotated_frame = result.plot()

            # Write the frame to the FFmpeg subprocess's stdin
            try:
                process.stdin.write(annotated_frame.tobytes())
            except (IOError, BrokenPipeError) as e:
                # This can happen if FFmpeg closes the pipe
                logging.error(f"FFmpeg process has closed. Terminating. Error: {e}")
                # Log FFmpeg's stderr for debugging
                if process.stderr is not None:
                    stderr_output = process.stderr.read().decode("utf-8")
                else:
                    stderr_output = "No stderr output available."

                logging.error(f"FFmpeg stderr:\n{stderr_output}")
                break

    except Exception as e:
        logging.error(f"Error during model tracking or streaming: {e}")
    finally:
        # Clean up the subprocess
        if process.stdin:
            process.stdin.close()
        process.wait()
        logging.info("FFmpeg process terminated.")
        logging.info("Script finished.")


if __name__ == "__main__":
    main()
