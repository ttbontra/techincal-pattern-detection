# ObjectDetectionApp.py
import sys

from PyQt5.QtGui import QPixmap, QPalette, QTextDocument
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPainter, QTextOption
from PyQt5.QtWidgets import  QTreeView, QStyleFactory, QStyledItemDelegate, QStyleOptionViewItem, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QComboBox, QTextEdit, QCheckBox, QScrollArea, QVBoxLayout, QTextBrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QComboBox, QTextEdit, QCheckBox, QScrollArea, QVBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QRect
import cv2
import os
import yaml
import numpy as np
import mss
import time
from PyQt5.QtGui import QImage, QPalette, QColor
from PyQt5.QtCore import pyqtSlot
import streamlit as st
#import torch
import json
from ultralytics import YOLO
from detect_objects import model as detection_model, detect_objects, color_map
from PyQt5.QtGui import QFont



class ObjectDetectionThread(QThread):
    changePixmap = pyqtSignal(QImage, list)

    def __init__(self, roi, model, color_map, *args, **kwargs):
        super(ObjectDetectionThread, self).__init__(*args, **kwargs)
        self.roi = roi
        self.model = model
        self.color_map = color_map
        self.running = True
       
        
    def run(self):
        with mss.mss() as sct:
            while self.running:
                sct_img = sct.grab(self.roi)
                frame = np.array(sct_img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Assuming detect_objects is adjusted to fit your PyQt app and returns correct detections
                frame, detected_objects = detect_objects(self.model, frame, color_map)

                # Convert frame for PyQt display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1000, 800, Qt.KeepAspectRatio)
                self.changePixmap.emit(p, detected_objects)  # Adapt based on your PyQt slot

                time.sleep(0.03)

    def stop(self):
        self.running = False

class ObjectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = self.loadModel()
        self.setWindowTitle("Object Detection Stream")
        self.setGeometry(100, 100, 1000, 600)  # x, y, width, height
        self.roi = None
        self.initUI()
        self.selectROI()
        self.lastDetectedObjects = []
    
    def loadModel(self):
        model_path = os.path.join('models', 'best.pt')  
        model =YOLO(model_path)
        return model

    def initUI(self):
        layout = QHBoxLayout()
        self.streamLabel = QLabel("Stream Display Here")
        layout.addWidget(self.streamLabel, 4)

        self.sidebarLayout = QVBoxLayout()  # Use a QVBoxLayout for the sidebar
        self.sectionSelector = QComboBox()
        self.sectionSelector.addItem("Select a section", None)  # Default option
        # Populate the dropdown with section names
        self.sectionSelector.addItem("Pattern Overview", "pattern_description")
        self.sectionSelector.addItem("Trading Strategy", "day_trading_strategy")
        self.sectionSelector.currentIndexChanged.connect(self.updateSidebarContent)  # Connect to update function
        self.sidebarLayout.addWidget(self.sectionSelector)

        self.sidebar = QTextBrowser()
        self.sidebarLayout.addWidget(self.sidebar)
        sidebarContainer = QWidget()
        sidebarContainer.setLayout(self.sidebarLayout)
        layout.addWidget(sidebarContainer, 1)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def selectROI(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Use the first monitor
            sct_img = sct.grab(monitor)
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            roi = cv2.selectROI("Select ROI", img, False, False)
            cv2.destroyAllWindows()
            if any(roi):  # Check if ROI is selected
                self.roi = {"top": roi[1], "left": roi[0], "width": roi[2], "height": roi[3]}
                self.startStreaming()

    def startStreaming(self):
        self.thread = ObjectDetectionThread(self.roi, self.model, color_map)
        self.thread.changePixmap.connect(self.updateGUI)
        self.thread.start()

    def loadHtmlContent(self, filename):
        try:
            with open(os.path.join('patterns', filename), 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
         
    #def loadHtmlContent(self, filename):
    #    try:
    #        with open(os.path.join('patterns', filename), 'r', encoding='utf-8') as file:
    #            return file.read()
    #    except FileNotFoundError:
    #        print(f"File {filename} not found.")
    #        return None

    @pyqtSlot(QImage, list)
    def updateGUI(self, image, detected_objects_with_colors):
        pixmap = QPixmap.fromImage(image)
        self.streamLabel.setPixmap(pixmap.scaled(self.streamLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Extract just the object names for comparison
        current_detected_object_names = [obj[0] for obj in detected_objects_with_colors]
        
        # Check if the detected objects have changed from the last update
        if set(current_detected_object_names) != set(self.lastDetectedObjects):
            self.updateSidebar(detected_objects_with_colors)
            self.lastDetectedObjects = current_detected_object_names


    #@pyqtSlot(QImage, list)
    #def updateGUI(self, image, detected_objects):
    #    pixmap = QPixmap.fromImage(image)
    #    self.streamLabel.setPixmap(pixmap.scaled(self.streamLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    #    self.updateSidebar(detected_objects)


    @pyqtSlot(QImage)  # Adjust according to the actual signal emitted
    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    # Ensure to stop the thread when closing the app
    def closeEvent(self, event):
        self.thread.stop()
        self.thread.wait()
        super().closeEvent(event)

    def updateSidebarContent(self, index):
        # Get the selected section name
        section_name = self.sectionSelector.currentData()
        if section_name:
            html_file_path = os.path.join("patterns", f"{section_name}.html")
            try:
                with open(html_file_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                    self.sidebar.setHtml(html_content)
            except FileNotFoundError:
                print(f"HTML file for {section_name} not found.")
                self.sidebar.setText(f"Content for {section_name} is not available.")

    def updateSidebar(self, detected_objects):
        # For this example, we'll just consider the first detected object
        if detected_objects:
            object_name = detected_objects[0]  # Assuming detected_objects is a list of object names
            html_file_path = os.path.join("strategy", f"{object_name.replace(' ', '_').lower()}.html")
            try:
                with open(html_file_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                    self.sidebar.setHtml(html_content)
            except FileNotFoundError:
                print(f"HTML file for {object_name} not found.")
                self.sidebar.setText(f"Summary for {object_name} is not available.")

def main():
    app = QApplication(sys.argv)
    ex = ObjectDetectionApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()