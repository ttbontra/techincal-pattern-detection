# main.py
#from PyQt5.QtWidgets import QApplication
#import sys
#from ObjectDetectionApp import ObjectDetectionApp

#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    mainWindow = ObjectDetectionApp()
#    mainWindow.show()
#    sys.exit(app.exec_())



# main.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from login_window import LoginWindow
from home_page import HomePage



def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Define dark color palette
    dark_palette = QPalette()
    
    # Base colors
    dark_palette.setColor(QPalette.Window, QColor(37, 37, 38))
    dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    dark_palette.setColor(QPalette.Base, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    
    # Text colors
    dark_palette.setColor(QPalette.Text, QColor(220, 220, 220))  # Editor text
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))  # Button background
    dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))  # Button text
    dark_palette.setColor(QPalette.BrightText, Qt.red)  # Bright text, for highlights
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    
    # Highlighting colors
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))  # Highlight background
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    
    app.setPalette(dark_palette)

    # Applying additional stylesheet for better dark theme support
    app.setStyleSheet("""
        QToolTip {
            color: #ffffff; 
            background-color: #2a82da; 
            border: 1px solid white;
        }
    """)

    login_window = LoginWindow()
    home_page = HomePage()

    def show_home_page():
        login_window.hide()
        home_page.show()

    login_window.login_successful.connect(show_home_page)

    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()