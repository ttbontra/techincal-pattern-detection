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
from login_window import LoginWindow
from home_page import HomePage


def main():
    app = QApplication(sys.argv)

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
