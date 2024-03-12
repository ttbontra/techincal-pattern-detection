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
