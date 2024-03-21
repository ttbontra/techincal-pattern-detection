# home_page.py
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QCheckBox, QFrame
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
                             QPushButton, QSpacerItem, QSizePolicy, QCheckBox, QLabel)
from PyQt5.QtCore import Qt
import os
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
#from PyQt5.QtGui import QPalette, QColor
from ObjectDetectionApp import ObjectDetectionApp
from PyQt5.QtWidgets import QCheckBox

color_map = {
    'consolidation': (0, 255, 0),
    'bullflag': (255, 105, 180),
    'mini bullflag': (0, 0, 255),
    'cup and handle': (255, 255, 255),
    'bearflag': (255, 0, 0),
    'mini bearflag': (255, 255, 0),
    'cloudbank': (0, 255, 255),
    'double bottom': (255, 0, 255),
    'double top': (0, 0, 0),
    'inverse cloudbank': (128, 128, 128),
    'scallop': (128, 0, 0),
    'inverse scallop': (0, 128, 0),

}

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 800, 600)
        self.sidebarVisible = True
        self.initUI()

    def initUI(self):
        
        self.mainLayout = QHBoxLayout(self)  # This is the primary layout of the window.

        # Sidebar setup
        self.sidebarFrame = QFrame()
        self.sidebarFrame.setFixedWidth(200)
        self.sidebarFrame.setStyleSheet("background-color: #1E1E1E;")
        self.sidebarLayout = QVBoxLayout(self.sidebarFrame)

        # Adding a title to the sidebar
        title = QLabel("Detectable Patterns")
        title.setFont(QFont("Arial", 14))
        title.setStyleSheet("color: white; margin: 10px 0;")
        self.sidebarLayout.addWidget(title)

        # Creating a scroll area for checkboxes to manage space effectively.
        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.addCheckboxes()

        self.sidebarLayout.addWidget(self.scrollArea)

        # Toggle Sidebar Button setup
        self.toggleSidebarButton = QPushButton()
        self.toggleSidebarButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'left.svg')))
        self.toggleSidebarButton.clicked.connect(self.toggleSidebar)
        self.toggleSidebarButton.setFixedSize(QSize(40, 40))  # Adjust size as needed
        self.toggleSidebarButton.setStyleSheet("QPushButton { border: none; }")

        # Button to run object detection
        objectDetectButton = QPushButton('Run Object Detection')
        objectDetectButton.clicked.connect(self.run_object_detection)
        objectDetectButton.setStyleSheet("font-size: 16px; background-color: #197422; color: white;")
        objectDetectButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Adding sidebar and content to the main layout
        self.mainLayout.addWidget(self.sidebarFrame)
        self.mainLayout.addWidget(self.toggleSidebarButton, 0, Qt.AlignTop)  # Ensure the button aligns to the top
        self.mainLayout.addWidget(objectDetectButton)

        # Set the application style
        QApplication.setStyle("Fusion")

    def addCheckboxes(self):
        options = [
            'consolidation', 'bullflag', 'mini bullflag', 'cup and handle',
            'bearflag', 'mini bearflag', 'cloudbank', 'double bottom',
            'double top', 'inverse cloudbank', 'scallop', 'inverse scallop'
        ]
        for option in options:
            checkBox = QCheckBox(option)
            checkBox.setStyleSheet("QCheckBox { color: white; }")
            checkBox.setChecked(True)
            checkBox.setEnabled(True)
            self.scrollLayout.addWidget(checkBox)


    def toggleSidebar(self):
        self.sidebarVisible = not self.sidebarVisible
        self.sidebarFrame.setVisible(self.sidebarVisible)
        iconPath = 'left.svg' if self.sidebarVisible else 'right.svg'
        self.toggleSidebarButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), iconPath)))


    def resizeEvent(self, event):
        super(HomePage, self).resizeEvent(event)
        # Ensure the toggle button is always centered vertically
        buttonX = 0 if not self.sidebarVisible else 200
        self.toggleSidebarButton.move(buttonX, self.height() // 2 - 20)

    def run_object_detection(self):
        # Make sure ObjectDetectionApp is defined elsewhere in your code
        self.objectDetectionWindow = ObjectDetectionApp()
        self.objectDetectionWindow.show()

def main():
    app = QApplication(sys.argv)
    homePage = HomePage()
    homePage.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()