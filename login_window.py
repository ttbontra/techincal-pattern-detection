import mysql.connector
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 280, 100)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.check_credentials)
        layout.addWidget(login_button)

        register_button = QPushButton('Register', self)
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def check_credentials(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Use your username
            password='stable',  # Use your password
            database='stocks'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (self.username.text(), self.password.text()))
        result = cursor.fetchone()

        if result:
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, 'Error', 'Bad username or password')

        connection.close()

    def register_user(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Use your username
            password='stable',  # Use your password
            database='stocks'
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (self.username.text(), self.password.text()))
        connection.commit()
        QMessageBox.information(self, 'Success', 'User registered successfully')

        connection.close()
