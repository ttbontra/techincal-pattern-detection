import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import cv2
import numpy as np
import mss
from ultralytics import YOLO
import os
from tkinter import Toplevel
from tkinter import Canvas

# Initialize YOLO model
model_path = os.path.join('models', 'best.pt')  # Update this path
model = YOLO(model_path)

color_map = {
    'consolidation': (0, 255, 0),
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255)
}

class ObjectDetectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Object Detection Stream")
        self.geometry("800x600")

        # Screen capture and ROI selection
        self.full_screen_image = None
        self.select_roi()

        # Streaming label
        self.stream_label = ctk.CTkLabel(self)
        self.stream_label.pack(expand=True, fill=tk.BOTH)

        # Start streaming in a separate thread
        self.streaming = False
        self.thread = threading.Thread(target=self.stream_roi)
        self.thread.daemon = True
        self.thread.start()

    def select_roi(self):
        # Capture the full screen
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Use the first monitor
            sct_img = sct.grab(monitor)
            img = Image.fromarray(np.array(sct_img))
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2RGB)
            self.full_screen_image = img

        # Display the full screen and let user select ROI
        roi = cv2.selectROI("Select ROI", self.full_screen_image, False, False)
        cv2.destroyAllWindows()
        self.roi = {"top": roi[1], "left": roi[0], "width": roi[2], "height": roi[3]}

    def stream_roi(self):
        with mss.mss() as sct:
            while True:
                if not self.roi:
                    continue
                sct_img = sct.grab(self.roi)
                frame = Image.fromarray(np.array(sct_img))
                frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGBA2RGB)

                # Apply object detection
                frame = detect_objects(model, frame, color_map)

                # Update GUI
                self.update_gui(frame)

    def update_gui(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.stream_label.configure(image=imgtk)
        self.stream_label.image = imgtk

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

if __name__ == "__main__":
    app = ObjectDetectionApp()
    app.mainloop()