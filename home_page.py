# home_page.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
import subprocess
import os
import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor
from ObjectDetectionApp import ObjectDetectionApp

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 300, 100)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        object_detect_button = QPushButton('Run Object Detection', self)
        object_detect_button.clicked.connect(self.run_object_detection)
        layout.addWidget(object_detect_button)

        self.setLayout(layout)

        # Set the application style to a sleek and modern style
        QApplication.setStyle(QStyleFactory.create("Fusion"))


    def run_object_detection(self):
        self.objectDetectionWindow = ObjectDetectionApp()
        self.objectDetectionWindow.show()

def main():
    app = QApplication(sys.argv)
    homePage = HomePage()
    homePage.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
