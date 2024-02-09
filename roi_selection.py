from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap
import sys
import cv2
import mss
import numpy as np
import time

class ObjectDetectionThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, roi, *args, **kwargs):
        super(ObjectDetectionThread, self).__init__(*args, **kwargs)
        self.roi = roi
        self.running = True

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
        self.roi = None
        self.initUI()
        self.selectROI()

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

    @pyqtSlot(QImage)
    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    # Ensure to stop the thread when closing the app
    def closeEvent(self, event):
        self.thread.stop()
        self.thread.wait()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    ex = ObjectDetectionApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
