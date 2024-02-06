import cv2
import numpy as np
import mss
import os
import pyautogui
from ultralytics import YOLO

# Load YOLO model
model_path = os.path.join('models','best.pt')  # Update this path
model = YOLO(model_path)

# Define a list of colors for bounding boxes
color_map = {
    'consolidation': (0, 255, 0),
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255)
}

# Capture the full screen
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Use the first monitor
    full_screen = np.array(sct.grab(monitor))
    full_screen = cv2.cvtColor(full_screen, cv2.COLOR_BGRA2BGR)

# Display the full screen for ROI selection
cv2.namedWindow('Select ROI', cv2.WINDOW_NORMAL)
roi = cv2.selectROI('Select ROI', full_screen, False, False)
cv2.destroyAllWindows()

# Define the ROI
roi = {"top": int(roi[1]), "left": int(roi[0]), "width": int(roi[2]), "height": int(roi[3])}

# Capture and process the selected ROI
with mss.mss() as sct:
    while True:
        img = np.array(sct.grab(roi))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Perform object detection
        results = model(img)[0]

        # Draw bounding boxes and labels
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            class_name = results.names[int(class_id)].lower()
            color = color_map.get(class_name, (255, 255, 255))

            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img, class_name.upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.imshow('Screen Capture with Object Detection', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
