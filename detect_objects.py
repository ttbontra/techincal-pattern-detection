# detect_objects.py
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import os

color_map = {
    'consolidation': (0, 255, 0), # Green
    'bullflag': (255, 105, 180), # purple
    'mini bullflag': (255, 0, 255), # Magenta
    'cup and handle': (255, 255, 255), # White
    'bearflag': (255, 100, 100), # Blue
    'mini bearflag': (255, 255, 0), # Yellow
    'cloudbank': (0, 255, 255), # Cyan
    'double bottom': (0, 0, 255), # Magenta
    'double top': (0, 0, 255), # White
    'inverse cloudbank': (128, 128, 128), # Gray
    'scallop': (128, 0, 0), # Maroon
    'inverse scallop': (0, 128, 0), # Green
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

#def detect_objects(model, img, color_map):
#        results = model(img)[0]
#        detected_objects = []  # Initialize a list to hold the names of detected objects
#        for result in results.boxes.data.tolist():
#            x1, y1, x2, y2, score, class_id = result
#            class_name = results.names[int(class_id)].lower()
#            detected_objects.append(class_name)  # Add detected class name to the list
#            color = color_map.get(class_name, (255, 255, 255))
#            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
#            cv2.putText(img, class_name.upper(), (int(x1), int(y1 - 10)),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
#        return img, detected_objects