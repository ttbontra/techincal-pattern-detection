# ObjectDetectionApp.py
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import  QTreeView, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import cv2
import os
import numpy as np
import mss
import time
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSlot

#import torch
import json
from ultralytics import YOLO
from detect_objects import detect_objects, color_map
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTreeView
#from strategy_loader import load_strategy_info

class ObjectDetectionThread(QThread):
    changePixmap = pyqtSignal(QImage, list)

    def __init__(self, roi, model, color_map, *args, **kwargs):
        super(ObjectDetectionThread, self).__init__(*args, **kwargs)
        self.roi = roi
        self.model = model
        self.color_map = color_map
        self.running = True
       
    #def __init__(self, roi, *args, **kwargs):
    #    super(ObjectDetectionThread, self).__init__(*args, **kwargs)
    #    self.roi = roi
    #    self.running = True
    #    self.model = model
    #    self.sidebar = QWidget()  # Create a sidebar widget
    #    self.sidebarLayout = QVBoxLayout()  # Create a layout for the sidebar
    #    self.sidebar.setLayout(self.sidebarLayout)

    #def loadModel(self):
    #    model_path = os.path.join('models', 'best.pt')  
    #    model =YOLO(model_path)
    #    return model
        
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
                p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
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
    
    def loadModel(self):
        model_path = os.path.join('models', 'best.pt')  
        model =YOLO(model_path)
        return model

    def initUI(self):
        self.setWindowTitle("Object Detection Stream")
        self.setGeometry(100, 100, 1000, 600)  # x, y, width, height
        #self.label = QLabel(self)
        #layout = QVBoxLayout()
        #layout.addWidget(self.label)
        #widget = QWidget()
        #widget.setLayout(layout)
        #self.setCentralWidget(widget)
        #self.sidebar = QWidget()  # Create a sidebar widget
        #self.sidebarLayout = QVBoxLayout()  # Create a layout for the sidebar
        #self.sidebar.setLayout(self.sidebarLayout)
        
        #from PyQt5.QtWidgets import QHBoxLayout  # Import QHBoxLayout from PyQt5.QtWidgets

        mainLayout = QVBoxLayout()
        self.label = QLabel(self)
        mainLayout.addWidget(self.label)
        self.sidebar = QWidget()
        self.sidebarLayout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebarLayout)
        self.sidebar.setFixedWidth(200)
        container = QWidget()
        container.setLayout(mainLayout)
        hLayout = QHBoxLayout()  # Fix: Import QHBoxLayout and create an instance
        hLayout.addWidget(container)
        hLayout.addWidget(self.sidebar)
        centralWidget = QWidget()
        centralWidget.setLayout(hLayout)  # Fix: Replace hLayout with container
        self.setCentralWidget(centralWidget)

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

    # Remove the redundant function definition
    def load_strategy_info(self, pattern_name):
         filename = os.path.join("strategy", f"{pattern_name}.json")
         try:
             with open(filename, 'r') as file:
                 return json.load(file)
         except FileNotFoundError:
             print(f"File {filename} not found.")
             return None

    @pyqtSlot(QImage, list)
    def updateGUI(self, image, detected_objects):
        # Update the main image display
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.updateSidebar(detected_objects)

    @pyqtSlot(QImage)  # Adjust according to the actual signal emitted
    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    #@pyqtSlot(QImage, list)
    #def setImage(self, image, detected_objects):
    #    pixmap = QPixmap.fromImage(image)
    #    self.label.setPixmap(pixmap)
    #    self.updateSidebar(detected_objects)

    # Ensure to stop the thread when closing the app
    def closeEvent(self, event):
        self.thread.stop()
        self.thread.wait()
        super().closeEvent(event)

    def updateSidebar(self, detected_objects):
        # Clear existing widgets from the sidebar layout
        for i in reversed(range(self.sidebarLayout.count())): 
            widget_to_remove = self.sidebarLayout.itemAt(i).widget()
            self.sidebarLayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Create a QTreeView and QStandardItemModel
        tree_view = QTreeView()
        model = QStandardItemModel()
        tree_view.setModel(model)

        # Load and display strategy information for each unique detected object
        unique_detected_objects = set(detected_objects)
        for object_name in unique_detected_objects:
            strategy_info = self.load_strategy_info(object_name.replace(" ", "_").lower())
            if strategy_info:
                # Create a QStandardItem for the object name
                object_item = QStandardItem(object_name)
                model.appendRow(object_item)

                # Create QStandardItems for pattern name, type, entry signal, and exit target
                pattern_name_item = QStandardItem(f"Pattern Name: {strategy_info['pattern_description']['name']}")
                pattern_type_item = QStandardItem(f"Pattern Type: {strategy_info['pattern_description']['type']}")
                entry_signal_item = QStandardItem(f"Entry Signal: {strategy_info['day_trading_strategy']['entry']['signal']}")
                exit_target_item = QStandardItem(f"Exit Target: {strategy_info['day_trading_strategy']['exit']['target']}")

                # Add the items as children of the object item
                object_item.appendRow([pattern_name_item, pattern_type_item, entry_signal_item, exit_target_item])

        # Add the tree view to the sidebar layout
        self.sidebarLayout.addWidget(tree_view)

def main():
    app = QApplication(sys.argv)
    ex = ObjectDetectionApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()