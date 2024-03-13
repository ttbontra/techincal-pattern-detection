# home_page.py
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QStyleFactory, QLabel, QSplitter, QListWidget, 
                             QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
import os
import sys

#from PyQt5.QtGui import QPalette, QColor
from ObjectDetectionApp import ObjectDetectionApp

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    #def initUI(self):
        # Main layout is horizontal: sidebar | main content
    #    mainLayout = QHBoxLayout(self)

        # Create a splitter for resizable sidebar
    #    splitter = QSplitter(Qt.Horizontal)
    #    mainLayout.addWidget(splitter)

        # Sidebar content
    #    self.sidebar = QListWidget()
    #    self.sidebar.addItem("Setting 1")
    #    self.sidebar.addItem("Setting 2")
    #    self.sidebar.addItem("Setting 3")
    #    splitter.addWidget(self.sidebar)

        # Main content area
    #    self.mainContent = QFrame(self)
    #    self.mainContent.setFrameShape(QFrame.StyledPanel)
    #    self.mainContentLayout = QVBoxLayout()

    #    object_detect_button = QPushButton('Run Object Detection', self)
    #    object_detect_button.clicked.connect(self.run_object_detection)
    #    self.mainContentLayout.addWidget(object_detect_button)

    #    self.mainContent.setLayout(self.mainContentLayout)
    #    splitter.addWidget(self.mainContent)

        # Adjust splitter sizes to make the sidebar initially smaller
    #    splitter.setSizes([200, 600])

    #    QApplication.setStyle(QStyleFactory.create("Fusion"))


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
