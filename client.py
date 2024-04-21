import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Initialize socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()), 9090))
enc = "utf-8"  # Encoding type

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(700, 800)
        input_style = """
            QLineEdit {
                font: bold 14px;
                background: transparent;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                color: black;
            }
            QLineEdit:focus {
                border: 3px solid #aaa;
            }
        """
        logo_path = r"C:\Users\hadib\OneDrive - American University of Beirut\Desktop\yallachat.jpg"  # Replace with the correct path
        background_label = QLabel(self)
        background_pixmap = QPixmap(logo_path)
        background_label.setPixmap(background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio))
        background_label.setScaledContents(True)
        background_label.resize(self.size())
        main_layout = QVBoxLayout(background_label)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setAlignment(Qt.AlignCenter)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)
        main_layout.addLayout(form_layout)
        login_button = QPushButton("Login")
        login_button.setStyleSheet("QPushButton { background: #ddd; border: none; padding: 10px; font-weight: bold; }")
        login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(login_button, alignment=Qt.AlignCenter)
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("QPushButton { background: #ddd; border: none; padding: 10px; font-weight: bold; }")
        signup_button.clicked.connect(self.open_signup_window)
        main_layout.addWidget(signup_button, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            message = f"login,{username},{password}"
            client.send(message.encode(enc))
            response = client.recv(1024).decode(enc)
            QMessageBox.information(self, "Login Response", response)
            if response == "Login Success!":
                QMessageBox.information(self, "Logged In", "You are now logged in.")
                self.close()

    def open_signup_window(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Signup")
        self.setFixedSize(700, 800)
        input_style = """
            QLineEdit {
                font: bold 14px;
                background: transparent;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 5px;
                color: black;
            }
            QLineEdit:focus {
                border: 3px solid #aaa;
            }
        """
        logo_path = r"C:\Users\hadib\OneDrive - American University of Beirut\Desktop\yallachat.jpg"  # Replace with the correct path
        background_label = QLabel(self)
        background_pixmap = QPixmap(logo_path)
        background_label.setPixmap(background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio))
        background_label.setScaledContents(True)
        background_label.resize(self.size())
        main_layout = QVBoxLayout(background_label)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setAlignment(Qt.AlignCenter)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(input_style)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)
        main_layout.addLayout(form_layout)
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("QPushButton { background: #ddd; border: none; padding: 10px; font-weight: bold; }")
        signup_button.clicked.connect(self.handle_signup)
        main_layout.addWidget(signup_button, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    def handle_signup(self):
        name = self.name_input.text()
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        if name and email and username and password:
            message = f"signup,{name},{email},{username},{password}"
            client.send(message.encode(enc))
            response = client.recv(1024).decode(enc)
            QMessageBox.information(self, "Signup Response", response)
            if response == "Signup Successful!":
                QMessageBox.information(self, "Signed Up", "You have successfully signed up.")
                self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
