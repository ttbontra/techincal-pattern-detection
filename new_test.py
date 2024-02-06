# This part remains unchanged
import cv2
import numpy as np
import mss
import os
from ultralytics import YOLO

# Function to initialize the model and ROI selection
def init_detection():
    model_path = os.path.join('models', 'best.pt')  # Update this path
    model = YOLO(model_path)
    return model

# Function to perform object detection on a frame
def detect_objects(model, img, color_map):
    results = model(img)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        class_name = results.names[int(class_id)].lower()
        color = color_map.get(class_name, (255, 255, 255))

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(img, class_name.upper(), (int(x1), int(y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    return img
