# main.py
from PyQt5.QtWidgets import QApplication
import sys
from ObjectDetectionApp import ObjectDetectionApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ObjectDetectionApp()
    mainWindow.show()
    sys.exit(app.exec_())
