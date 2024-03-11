# home_page.py
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor

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

        # Set the color palette for dark mode
        #dark_palette = QPalette()
        #dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        #dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        #dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        #dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        #dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        #dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        #dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        #dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        #dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        #dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        #dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        #dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        #dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        #QApplication.setPalette(dark_palette)

        # Uncomment the following line to use the system default color palette
        # QApplication.setPalette(QApplication.style().standardPalette())

    def run_object_detection(self):
        script_path = os.path.join(os.path.dirname(__file__), 'ObjectDetectionApp.py')
        # Specify the full path to the correct Python executable
        python_executable = 'C:\\Users\\ttbon\\Documents\\technical_pattern_detection\\.venv\\Scripts\\python.exe'  # Adjust this path
        try:
            result = subprocess.run([python_executable, script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error:", e.stderr)
            print("The script exited with status code", e.returncode)
