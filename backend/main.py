from ultralytics import YOLO

model = YOLO("yoloModels/rtdetr-x.pt")

# fourcc = cv2.VideoWriter.fourcc(*'H264')

# output_url = 'http://localhost:8080/live/livestream.flv'
# out = cv2.VideoWriter(output_url, fourcc, 30, (1920, 1080))

results = model.track('rtmp://localhost/live/livestream', stream=True, tracker="bytetrack.yaml")

import logging
logging.basicConfig(level=logging.ERROR)

try:
    for result in results:
        try:
            annotated_frame = result.plot()
#             out.write(annotated_frame)
        except Exception as e:
            logging.error(f"Error processing frame: {e}")
            # Optionally, break or continue depending on desired behavior
            continue
# 
#     out.release()
except Exception as e:
    logging.error(f"Error in streaming or model inference: {e}")