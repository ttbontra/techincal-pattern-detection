# home_page.py
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout

from PyQt5.QtCore import Qt
import os
import sys

#from PyQt5.QtGui import QPalette, QColor
from ObjectDetectionApp import ObjectDetectionApp


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

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        
        main_layout = QVBoxLayout()  # The main layout

        # Create horizontal layout with spacers to center the button horizontally
        h_layout = QHBoxLayout()
        spacer_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        object_detect_button = QPushButton('Run Object Detection', self)
        object_detect_button.clicked.connect(self.run_object_detection)
        # Adjust the button size and policy
        object_detect_button.setMinimumSize(250, 20)  # width, height
        object_detect_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)

        # Add widgets and spacers to the horizontal layout
        h_layout.addItem(spacer_left)
        h_layout.addWidget(object_detect_button)
        h_layout.addItem(spacer_right)

        # Spacers to push the layout containing the button to the middle vertically
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add the top spacer, the horizontal layout, and the bottom spacer to the main layout
        main_layout.addItem(spacer_top)
        main_layout.addLayout(h_layout)
        main_layout.addItem(spacer_bottom)

        self.setLayout(main_layout)

        # Set the application style
        QApplication.setStyle("Fusion")


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