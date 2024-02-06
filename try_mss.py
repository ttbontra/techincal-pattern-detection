import cv2
import numpy as np
import mss
import pyautogui

# Global variables
roi_selected = False
x1, y1, x2, y2 = 0, 0, 0, 0

def on_mouse(event, x, y, flags, params):
    global x1, y1, x2, y2, roi_selected
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        roi_selected = False
    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        roi_selected = True

# Capture the full screen
with mss.mss() as sct:
    monitor = sct.monitors[1]  # Use the first monitor
    full_screen = np.array(sct.grab(monitor))
    full_screen = cv2.cvtColor(full_screen, cv2.COLOR_BGRA2BGR)

# Display the full screen for ROI selection
cv2.namedWindow('Select ROI', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Select ROI', on_mouse)

while True:
    img = full_screen.copy()
    if roi_selected:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow('Select ROI', img)

    key = cv2.waitKey(1)
    if key == ord('q') or roi_selected:
        break

cv2.destroyAllWindows()

# Ensure valid ROI coordinates
x1, y1, x2, y2 = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

# Define the ROI
roi = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}

# Capture and display the selected ROI
with mss.mss() as sct:
    while True:
        img = np.array(sct.grab(roi))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imshow('ROI Capture', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
