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




class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 800, 600)
        self.sidebarVisible = True
        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout(self)

        self.sidebarFrame = QFrame()
        self.sidebarFrame.setFixedWidth(200)
        self.sidebarFrame.setStyleSheet("background-color: #1E1E1E;")
        self.sidebarLayout = QVBoxLayout()

        title = QLabel("Detectable Patterns")
        title.setFont(QFont("Arial", 14))
        title.setStyleSheet("color: white; margin: 10px 0;")
        self.sidebarLayout.addWidget(title)

        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout()
        self.scrollWidget.setLayout(self.scrollLayout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.sidebarLayout.addWidget(self.scrollArea)

        self.sidebarFrame.setLayout(self.sidebarLayout)
        self.mainLayout.addWidget(self.sidebarFrame)

        self.addPatternLabels()

        self.toggleSidebarButton = QPushButton()
        self.toggleSidebarButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'left.svg')))
        self.toggleSidebarButton.clicked.connect(self.toggleSidebar)
        self.toggleSidebarButton.setFixedSize(QSize(40, 40))
        self.toggleSidebarButton.setStyleSheet("QPushButton { border: none; }")
        self.mainLayout.addWidget(self.toggleSidebarButton, 0, Qt.AlignTop)

        objectDetectButton = QPushButton('Run Object Detection')
        objectDetectButton.clicked.connect(self.run_object_detection)
        objectDetectButton.setStyleSheet("font-size: 16px; background-color: #197422; color: white;")
        objectDetectButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.mainLayout.addWidget(objectDetectButton)

        QApplication.setStyle("Fusion")
        self.setLayout(self.mainLayout)

    def addPatternLabels(self):
        patterns = [
            'consolidation', 'bullflag', 'mini bullflag', 'cup and handle',
            'bearflag', 'mini bearflag', 'cloudbank', 'double bottom',
            'double top', 'inverse cloudbank', 'scallop', 'inverse scallop'
        ]
        for pattern in patterns:
            label = QLabel(pattern)
            label.setStyleSheet("QLabel { color: white; }")
            self.scrollLayout.addWidget(label)

    def addCheckboxes(self):
        self.checkboxes = []
        options = [
            'consolidation', 'bullflag', 'mini bullflag', 'cup and handle',
            'bearflag', 'mini bearflag', 'cloudbank', 'double bottom',
            'double top', 'inverse cloudbank', 'scallop', 'inverse scallop'
        ]
        for option in options:
            checkBox = QCheckBox(option)
            checkBox.setStyleSheet("QCheckBox { color: white; }")
            checkBox.setChecked(True)  # Default to checked
            self.checkboxes.append(checkBox)  # Keep track of the checkboxes
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

    def getSelectedObjectTypes(self):
        selected_types = []
        for checkbox in self.findChildren(QCheckBox):  # Assuming checkboxes are direct children
            if checkbox.isChecked():
                selected_types.append(checkbox.text())
        return selected_types

    #def run_object_detection(self):
    #    # Make sure ObjectDetectionApp is defined elsewhere in your code
    #    self.objectDetectionWindow = ObjectDetectionApp()
    #    self.objectDetectionWindow.show()

def main():
    app = QApplication(sys.argv)
    homePage = HomePage()
    homePage.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()