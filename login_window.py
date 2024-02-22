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
        login_button.clicked.connect(self.check_credentials)
        layout.addWidget(login_button)

        register_button = QPushButton('Register', self)
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def check_credentials(self):
        data = json.dumps({
            "username": self.username.text(),
            "password": self.password.text()
        }).encode('utf-8')

        request = QNetworkRequest(QUrl("http://127.0.0.1:8000/login"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        reply = self.network_manager.post(request, data)
        reply.finished.connect(self.on_login_response)

    def on_login_response(self):
        reply = self.sender()
        err = reply.error()

        if err == QNetworkReply.NoError:
            if reply.url().toString().endswith("/login"):
                self.login_successful.emit()
                self.hide()
                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
        else:
            QMessageBox.critical(self, "Error", "You do not have a valid subscription. Please sign up to use this service.")

    def register_user(self):
        data = json.dumps({
            "username": self.username.text(),
            "password": self.password.text(),
            "email": self.email.text()
        }).encode('utf-8')

        request = QNetworkRequest(QUrl("http://127.0.0.1:8000/signup"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        reply = self.network_manager.post(request, data)
        reply.finished.connect(self.on_signup_response)

    def on_signup_response(self):
        reply = self.sender()
        err = reply.error()

        if err == QNetworkReply.NoError:
            if reply.url().toString().endswith("/signup"):
                QMessageBox.information(self, "Signup Successful", "You have successfully signed up.")
                # Redirect to webpage for subscription purchase
                QDesktopServices.openUrl(QUrl("https://github.com/ttbontra/techincal-pattern-detection/blob/main/login_window.py"))
        else:
            QMessageBox.critical(self, "Error", "You do not have a valid subscription. Please sign up to use this service.")
