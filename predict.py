import os
#import time
from ultralytics import YOLO
import cv2
#import numpy as np

VIDEOS_DIR = os.path.join('videos')

video_path = os.path.join(VIDEOS_DIR, 'test_cut.mp4')
output_path = '{}_output.mp4'.format(video_path)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise IOError("Error opening video file. Check the file path and format.")
ret, frame = cap.read()
if not ret:
    raise Exception("Could not read the first frame from the video.")

H, W, _ = frame.shape
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))
#fps = cap.get(cv2.CAP_PROP_FPS)

model_path = os.path.join('models','best.pt')
model = YOLO(model_path)

# Define a list of colors for bounding boxes
color_map = {
    'consolidation': (0, 255, 0),   
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255)     
}

threshold = 0.0000000000001 # threshold for detection confidences

while ret:

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        class_name = results.names[int(class_id)].lower()
        color = color_map.get(class_name, (255, 255, 255))

        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, .5)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, .5, color, .5)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()