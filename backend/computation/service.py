import cv2
import asyncio
import subprocess
import logging
from sqlalchemy.sql import false
from ultralytics import YOLO
import sys
import os
from database import persist_data

# Project root path zu dem Skript hinzufügen, damit ich die Module importieren kann
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# --- Configuration ---
MODEL_PATH = "yoloModels/yolov8n.pt"
# INPUT_URL = "rtmp://fnstream.westeurope.cloudapp.azure.com/live/kassim"
# OUTPUT_URL = "rtmp://fnstream.westeurope.cloudapp.azure.com/live/output"
INPUT_URL = "rtmp://localhost/live/livestream"
OUTPUT_URL = "rtmp://localhost/live/output"


async def main():
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

    # --- RTMP Stream Fetchen ---
    # Liest aus dem input daten wie die Auflösung, FPS etc. aus damit
    # die Ausgabe entsprechend angepasst werden kann.
    # Das ist wichtig damit es nicht zu Problemen mit der Ausgabe kommt,
    # wenn die Auflösung oder FPS zu hoch ist.
    cap = cv2.VideoCapture(INPUT_URL)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()

    logging.info(f"Input stream properties: {width}x{height} @ {fps} FPS")

    # --- RTMP zu FLV umwandeln mit FFmpeg ---
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
        str(fps),
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
        str(fps * 2),
        "-keyint_min",
        str(fps * 2),
        "-sc_threshold",
        "0",
        "-f",
        "flv",
        OUTPUT_URL,
    ]

    # Start the FFmpeg subprocess
    try:
        # Hier wird der Subprocess gestartet und die stdin und stderr werden geöffnet, damit wir die annotierten Frames an FFmpeg senden können
        process = subprocess.Popen(
            ffmpeg_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # stdin bedeutet dass wir die Daten an FFmpeg senden können,
        # stderr bedeutet dass wir die Fehlermeldungen von FFmpeg lesen können
        if process.stdin is None:
            logging.error("Failed to open stdin for FFmpeg subprocess.")
            return

        logging.info("Started FFmpeg subprocess for streaming.")

    # Error Handling für den Fall dass FFmpeg nicht gefunden wird oder der Subprocess nicht gestartet werden kann
    except FileNotFoundError:
        logging.error(
            "FFmpeg not found. Please ensure it is installed and in your PATH."
        )
        return
    except Exception as e:
        logging.error(f"Failed to start FFmpeg subprocess: {e}")
        return

    # -- Computation process ---
    # An dieser stelle haben wir dann den FFmpeg Prozess gestartet und können jetzt die Frames von der YOLO Segmentierung an FFmpeg senden.
    try:
        # Track verwenden damit die results der Segmentiertung mit einer ID versehen werden und es nicht zu Duplikaten kommnt
        results = model.track(source=INPUT_URL, stream=True, tracker="bytetrack.yaml")

        for result in results:
            # plot() gibt das result aus der Segmentierung zurück, also die annotierten Frames mit den Bounding Boxes,
            # Labels und IDs
            annotated_frame = result.plot()

            # Failed to write rresult to JSON file: 'Results' object has no attribute 'all'
            try:
                await persist_data.add_results(result)
                logging.info("Successfully persisted data to database.")
            except Exception as e:
                logging.error(f"Failed to persist data to database: {e}")

            # Write the frame to the FFmpeg subprocess's stdin
            try:
                process.stdin.write(annotated_frame.tobytes())

            # Error handling für den Fall dass FFmpeg die Verbindung geschlossen hat oder es zu einem Fehler beim Schreiben kommt
            except (IOError, BrokenPipeError) as e:
                # This can happen if FFmpeg closes the pipe
                logging.error(f"FFmpeg process has closed. Terminating. Error: {e}")

                # Falls mein Prozess einen fehler hat wird der in stderr ausgelesen und geloggt, damit ich weiß was schief gelaufen ist
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


# Entry point Guard schützt das meine funktion nur ausgeführt wird wenn ich das Skript direkt ausführe
if __name__ == "__main__":
    asyncio.run(main())
