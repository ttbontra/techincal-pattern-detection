# ObjectDetectionApp.py
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import cv2
import os
import numpy as np
import mss
import time
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
import torch
from ultralytics import YOLO

class ObjectDetectionThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, roi, *args, **kwargs):
        super(ObjectDetectionThread, self).__init__(*args, **kwargs)
        self.roi = roi
        self.running = True
        self.sidebar = QWidget()  # Create a sidebar widget
        self.sidebarLayout = QVBoxLayout()  # Create a layout for the sidebar
        self.sidebar.setLayout(self.sidebarLayout)

    def run(self):
        with mss.mss() as sct:
            while self.running:
                if self.roi:
                    monitor = {"top": self.roi['top'], "left": self.roi['left'], "width": self.roi['width'], "height": self.roi['height']}
                    sct_img = sct.grab(monitor)
                    img = np.array(sct_img)

                    # Simulate object detection
                    # Replace this part with actual YOLO detection
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format
                    # img, detected_objects = detect_objects(yolo_model, img)

                    # Convert to QImage
                    h, w, ch = img.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(img.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                time.sleep(0.03)  # Limit the frame rate

    def stop(self):
        self.running = False

class ObjectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = self.loadModel()
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
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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
        self.thread = ObjectDetectionThread(self.roi)
        self.thread.changePixmap.connect(self.setImage)
        self.thread.start()

    @pyqtSlot(QImage, list)
    def setImage(self, image, detected_objects):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
        self.updateSidebar(detected_objects)

    # Ensure to stop the thread when closing the app
    def closeEvent(self, event):
        self.thread.stop()
        self.thread.wait()
        super().closeEvent(event)

    def updateSidebar(self, detected_objects):
    # Clear the existing content in the sidebar
        for i in reversed(range(self.sidebarLayout.count())): 
            widgetToRemove = self.sidebarLayout.itemAt(i).widget()
            self.sidebarLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        # Update the sidebar with new detected objects
        if detected_objects:
            for object_name in detected_objects:
                # Create a label for each detected object
                label = QLabel(object_name.capitalize())
                self.sidebarLayout.addWidget(label)
                # Here, you could also add buttons or links to display more information
        else:
            label = QLabel("No objects detected.")
            self.sidebarLayout.addWidget(label)

def main():
    app = QApplication(sys.argv)
    ex = ObjectDetectionApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
