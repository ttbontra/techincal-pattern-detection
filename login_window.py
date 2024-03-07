import mysql.connector
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QUrl

from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json
from PyQt5.QtGui import QDesktopServices

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 280, 100)
        self.initUI()
        self.network_manager = QNetworkAccessManager()  # Add network_manager attribute
        self.csrf_token = None 

    def initUI(self):
        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Email')
        layout.addWidget(self.email)

        login_button = QPushButton('Login', self)
        #login_button.clicked.connect(self.check_credentials)
        login_button.clicked.connect(self.fetch_csrf_token)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def fetch_csrf_token(self):
        request = QNetworkRequest(QUrl("http://127.0.0.1:8000/accounts/login/"))
        reply = self.network_manager.get(request)
        reply.finished.connect(self.on_csrf_token_received)

    def on_csrf_token_received(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            cookies = self.network_manager.cookieJar().cookiesForUrl(QUrl("http://127.0.0.1:8000/accounts/login/"))
            for cookie in cookies:
                if cookie.name() == b'csrftoken':
                    # Convert QByteArray to Python byte string and then decode
                    self.csrf_token = bytes(cookie.value()).decode('utf-8')
                    self.check_credentials()  # Now you can proceed to check credentials
                    break
        reply.deleteLater()



    def check_credentials(self):
        data = json.dumps({
            "username": self.username.text(),
            "password": self.password.text()
        }).encode('utf-8')

        request = QNetworkRequest(QUrl("http://127.0.0.1:8000/accounts/login/"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"X-CSRFToken", self.csrf_token.encode('utf-8'))

        reply = self.network_manager.post(request, data)
        reply.finished.connect(self.on_login_response)

    def on_login_response(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            if reply.url().toString().endswith("accounts/login/"):
                self.login_successful.emit()
                self.hide()
                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
            # Handle successful login
            pass
        else:
            QMessageBox.critical(self, "Error", "You do not have a valid subscription. Please sign up to use this service.")
            # Handle login failure
            pass
        reply.deleteLater()

#    def on_login_response(self):
#        reply = self.sender()
#        err = reply.error()

#        if err == QNetworkReply.NoError:
#            if reply.url().toString().endswith("accounts/login/"):
#                self.login_successful.emit()
#                self.hide()
#                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
#        else:
#            QMessageBox.critical(self, "Error", "You do not have a valid subscription. Please sign up to use this service.")


    def on_signup_response(self):
        reply = self.sender()
        err = reply.error()

        if err == QNetworkReply.NoError:
            if reply.url().toString().endswith("/register"):
                QMessageBox.information(self, "Signup Successful", "You have successfully signed up.")
                # Redirect to webpage for subscription purchase
                QDesktopServices.openUrl(QUrl("https://github.com/ttbontra/techincal-pattern-detection/blob/main/login_window.py"))
        else:
            QMessageBox.critical(self, "Error", "You do not have a valid subscription. Please sign up to use this service.")
