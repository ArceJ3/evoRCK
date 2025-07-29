from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QLineEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from views.secondary_window import SecondaryWindow


class LoginWindow(QMainWindow):
    """Login Window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("evoReckon")
        self.setGeometry(100, 100, 700, 400)
        self.setFixedSize(700, 400)

        self.secondary_window = SecondaryWindow()

        self.background_label = QLabel(self)
        pixmap = QPixmap("src/img/evRck.jpg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())
        self.background_label.lower()

        central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(central_layout)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_widget.setLayout(form_layout)

        self.label = QLabel("Welcome to evoReckon")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 30px;
            }
        """)

        form_layout.addWidget(self.label)
        form_layout.addSpacing(80)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setFixedWidth(250)
        self.user_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #aaa;
                color: black;
                }
                QLineEdit:placeholder {
                    color: gray;
                }""")
        
        form_layout.addWidget(self.user_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addSpacing(30)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedWidth(250)
        self.pass_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #aaa;
                color: black;
                }
                QLineEdit:placeholder {
                    color: gray;
                }""")
        form_layout.addWidget(self.pass_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addSpacing(50)

        self.button = QPushButton("Login")
        self.button.setFixedSize(120, 40)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: darkblue;
            }
        """)
        form_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_layout.addStretch()
        central_layout.addWidget(form_widget)

        self.button.clicked.connect(self.on_button_click)

    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())
        super().resizeEvent(event)

    def on_button_click(self):
        self.hide()
        self.secondary_window.show()
