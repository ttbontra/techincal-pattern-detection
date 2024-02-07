from collections import Counter
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
model_path = os.path.join('models', 'best.pt')  
model = YOLO(model_path)

color_map = {
    'consolidation': (0, 255, 0),
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255),
    'cup and handle': (255, 255, 255),
    'bearflag': (255, 0, 0),
    'mini bearflag': (255, 255, 0),
    'cloudbank': (0, 255, 255),
}

class ObjectDetectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Object Detection Stream")
        self.geometry("1000x600")  # Increased width to accommodate sidebar

        # Screen capture and ROI selection
        self.full_screen_image = None
        self.select_roi()

        # Main frame for streaming
        self.stream_frame = ctk.CTkFrame(self, width=800, height=600)
        self.stream_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sidebar for object summary
        self.sidebar_frame = ctk.CTkFrame(self, width=200, height=600)
        self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Detected Objects:", anchor="nw", justify=tk.LEFT)
        self.sidebar_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Streaming label
        self.stream_label = ctk.CTkLabel(self.stream_frame)
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

                # Apply object detection and capture detected object names
                frame, detected_objects = detect_objects(model, frame, color_map)

                # Update GUI with the frame and detected objects
                self.update_gui(frame, detected_objects)


    def update_gui(self, frame, detected_objects):
    # Ensure frame is a valid image array
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.stream_label.configure(image=imgtk)
            self.stream_label.image = imgtk

            # Additionally, update the sidebar with detected object summaries
            self.update_sidebar(detected_objects)
    
    def update_sidebar(self, detected_objects):
        # Count the occurrences of each detected object
        object_counts = Counter(detected_objects)
        
        # Prepare the text to display in the sidebar
        sidebar_text = "Detected Objects:\n"
        for object_name, count in object_counts.items():
            sidebar_text += f"{object_name}: {count}\n"
        
        # Update the sidebar_label with the new text
        self.sidebar_label.configure(text=sidebar_text)

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


if __name__ == "__main__":
    app = ObjectDetectionApp()
    app.mainloop()