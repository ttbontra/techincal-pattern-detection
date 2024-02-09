# detect_objects.py
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os

color_map = {
    'consolidation': (0, 255, 0),
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255),
    'cup and handle': (255, 255, 255),
    'bearflag': (255, 0, 0),
    'mini bearflag': (255, 255, 0),
    'cloudbank': (0, 255, 255),
}

model_path = os.path.join('models', 'best.pt')  
model = YOLO(model_path)

def detect_objects(model, img, color_map):
        results = model(img)[0]
        detected_objects = []  # Initialize a list to hold the names of detected objects
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            class_name = results.names[int(class_id)].lower()
            detected_objects.append(class_name)  # Add detected class name to the list
            color = color_map.get(class_name, (255, 255, 255))
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img, class_name.upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return img, detected_objects


