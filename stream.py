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
import json
import random
from tkinter import Label



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
        self.stream_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  

        # Sidebar for object summary
        #self.sidebar_frame = ctk.CTkFrame(self, width=200, height=600)
        #self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)  # Changed side to LEFT
        #self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Detected Objects:", anchor="nw", justify=tk.LEFT)
        #self.sidebar_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.sidebar_frame = tk.Frame(self, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.sidebar_content_frame = tk.Frame(self.sidebar_frame)
        self.sidebar_content_frame.pack(fill=tk.BOTH, expand=True)
        self.expandable_frames = {}

        # Streaming label
        self.stream_label = ctk.CTkLabel(self.stream_frame)
        self.stream_label.pack(expand=True, fill=tk.BOTH)
        #self.image_label = Label(self)  # Changed from ctk.CTkLabel to tkinter Label
        #self.image_label.pack(expand=True, fill=tk.BOTH)

        # Start streaming in a separate thread
        self.streaming = False
        self.thread = threading.Thread(target=self.stream_roi)
        self.thread.daemon = True
        self.thread.start()

    def simulate_detection():
        # Example objects that might be detected
        possible_objects = ['consolidation', 
                            'bullflag', 
                            'bearflag', 
                            'cup and handle', 
                            'cloudbank',
                            'mini bullflag',
                            'mini bearflag']
        detected_objects = [random.choice(possible_objects) for _ in range(random.randint(1, 10))]
        return detected_objects
    

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

    def load_strategy_info(self, pattern_name):
        filename = os.path.join("strategy", f"{pattern_name}.json")  # Assuming the file is named after the pattern
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
    
    #def update_sidebar(self, detected_objects):
    #    if detected_objects:
            # Count the occurrences of each detected object
    #        object_counts = Counter(detected_objects)
            
            # Initialize sidebar text with a header
    #        sidebar_text = "Detected Patterns:\n\n"
            
            # Append each unique detected object and its count to the sidebar text
    #        for object_name, count in object_counts.items():
    #            sidebar_text += f"{object_name.title()}: {count}\n"
            
            # Update the sidebar label with the new text
    #        self.sidebar_label.configure(text=sidebar_text)
    #    else:
            # Update the sidebar label to indicate no objects were detected
    #        self.sidebar_label.configure(text="No patterns detected.")

    def update_sidebar(self, detected_objects):
        # Clear previous sidebar content
        for widget in self.sidebar_content_frame.winfo_children():
            widget.destroy()

        self.expandable_frames = {}

        if detected_objects:
            # Example detected_objects list for demonstration
            # detected_objects = ['pattern1', 'pattern2', ...]
            for object_name in set(detected_objects):  # Using set for unique elements
                self.create_expandable_section(object_name)
        else:
            label = tk.Label(self.sidebar_content_frame, text="No patterns detected.")
            label.pack()

 

    def create_expandable_section(self, pattern_name):
        # Button toggles the visibility of its associated detail_frame
        button = tk.Button(self.sidebar_content_frame, text=pattern_name, command=lambda: self.toggle_pattern_details(pattern_name))
        button.pack(fill=tk.X)

        # Frame for detailed information, initially hidden
        detail_frame = tk.Frame(self.sidebar_content_frame, height=0)
        detail_frame.pack(fill=tk.X, pady=5)
        detail_frame.pack_propagate(False)  # Prevent frame from resizing to its content

        self.expandable_frames[pattern_name] = detail_frame

    def toggle_pattern_details(self, pattern_name):
        detail_frame = self.expandable_frames.get(pattern_name)
        
        # Clear existing content in the detail frame (if any)
        for widget in detail_frame.winfo_children():
            widget.destroy()

        # Load the pattern's strategy information from JSON
        strategy_info = self.load_strategy_info(pattern_name.lower().replace(" ", "_"))  # Adjust naming convention as needed

        if strategy_info:
            pattern_description = strategy_info.get("pattern_description", {})
            day_trading_strategy = strategy_info.get("day_trading_strategy", {})

            # Creating text to display
            display_text = f"Name: {pattern_description.get('name', 'N/A')}\n"
            display_text += f"Type: {pattern_description.get('type', 'N/A')}\n"
            display_text += f"Appearance: {pattern_description.get('appearance', 'N/A')}\n"
            display_text += f"Significance: {pattern_description.get('significance', 'N/A')}\n\n"
            display_text += "Day Trading Strategy:\n"
            display_text += f"Entry Signal: {day_trading_strategy.get('entry', {}).get('signal', 'N/A')}\n"
            display_text += f"Confirmation: {day_trading_strategy.get('entry', {}).get('confirmation', 'N/A')}\n"
            display_text += f"Exit Target: {day_trading_strategy.get('exit', {}).get('target', 'N/A')}\n"
            display_text += f"Stop Loss: {day_trading_strategy.get('exit', {}).get('stop_loss', 'N/A')}\n"
            display_text += f"Position Size: {day_trading_strategy.get('risk_management', {}).get('position_size', 'N/A')}\n"
            display_text += f"Profit Booking: {day_trading_strategy.get('risk_management', {}).get('profit_booking', 'N/A')}\n"
            display_text += f"Considerations: {day_trading_strategy.get('considerations', {}).get('volume', 'N/A')}; "
            display_text += f"False Breakouts: {day_trading_strategy.get('considerations', {}).get('false_breakouts', 'N/A')}; "
            display_text += f"Market Conditions: {day_trading_strategy.get('considerations', {}).get('market_conditions', 'N/A')}"

            # Use a Text widget or similar to display the information
            text_widget = tk.Text(detail_frame, height=20, width=50)
            text_widget.pack(expand=True, fill=tk.BOTH)
            text_widget.insert(tk.END, display_text)
            text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

            # Adjust the frame's visibility
            detail_frame.pack(fill=tk.BOTH, expand=True)
            detail_frame.pack_propagate(False)
        else:
            # Hide the detail frame if no strategy info is found
            detail_frame.pack_forget()

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