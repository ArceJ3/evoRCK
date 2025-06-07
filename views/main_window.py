# main_window.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from views.secondary_window import SecondaryWindow  # Asegúrate de importar la clase correcta

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Reckon App")
        self.setGeometry(100, 100, 400, 300)

        # Crear una instancia de la ventana secundaria
        self.secondary_window = SecondaryWindow()

        # Configurar fondo
        self.background_label = QLabel(self)
        pixmap = QPixmap("src/img/evRck.jpg")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(self.rect())
        self.background_label.lower()

        central_widget = QWidget(self)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        self.label = QLabel("¡Bienvenido a evoTrack!")
        self.label.setStyleSheet("color: black; font-weight: bold;")
        self.label2 = QLabel("Estado de Botón:")
        self.label2.setStyleSheet("color: black;")

        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        layout.addStretch()

        button_layout = QHBoxLayout()
        self.button = QPushButton("Recibir")
        self.button.setFixedSize(120, 40)
        self.button2 = QPushButton("Entregar")
        self.button2.setFixedSize(120, 40)

        self.button.setStyleSheet("background-color: red; color: white;")
        button_layout.addWidget(self.button)
        button_layout.addWidget(self.button2)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_layout)

        self.button.clicked.connect(self.on_button_click)
        self.button2.clicked.connect(self.on_button_click2)

    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())
        super().resizeEvent(event)

    def on_button_click(self):
        self.label2.setText("Estado de Botón: \n ¡Botón Recibir presionado!")
        self.hide()  # Oculta esta ventana
        self.secondary_window.show()  # Muestra la secundaria

    def on_button_click2(self):
        self.label2.setText("Estado de Botón: \n ¡Botón Entregar presionado!")
