from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class CustomReasonDialog(QDialog):
    def __init__(self, mode: str, fur_code: str, cantidad: str, parent=None):
        super().__init__(parent)

        self.fur_code = fur_code
        self.cantidad = cantidad
        self.mode = mode
    
        self.setWindowTitle(f"{mode}")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        # --- Imagen basada en FUR CODE ---
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = os.path.join("src", "table_layouts", f"{fur_code}.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.image_label.setText("No image available")
        
        layout.addWidget(self.image_label)

        label_fur = QLabel(f"FUR CODE: {fur_code}")
        label_cantidad = QLabel(f"Quantity: {cantidad}")
        label_info = QLabel("Please select a reason:")
        label_info.setStyleSheet("margin-top: 10px; font-weight: bold")

        self.combo_reason = QComboBox()
        self.combo_reason.addItem("--- Select a reason ---")
        if mode == "add" or mode == "add_new":
            self.combo_reason.addItems(["PUR", "PROJECT"])
        elif mode == "substract":
            self.combo_reason.addItems(["MAINTENANCE", "SCHEDULED", "MIGRATION"])

        layout.addWidget(label_fur)
        layout.addWidget(label_cantidad)
        layout.addWidget(label_info)
        layout.addWidget(self.combo_reason)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.mostrar_confirmacion)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

    def mostrar_confirmacion(self):
        if self.combo_reason.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "Invalid option.")
            return

        msg = QMessageBox(self)  # padre = este diálogo, para que no desaparezca
        msg.setWindowTitle("Confirm")
        msg.setText(f"Do you want to {self.mode.upper()}?\n\n"
                    f"FUR CODE: {self.fur_code}\n"
                    f"Quantity: {self.cantidad}\n"
                    f"Reason: {self.combo_reason.currentText()}")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.buttonClicked.connect(self.procesar_respuesta)
        msg.open()

    def procesar_respuesta(self, button):
        if button.text() == "&Yes" or button.text() == "Yes":
            self.ok = True
            self.accept() 
        else:
            # Si cancela, solo retorna y mantiene abierto
            pass

    def get_reason(self):
        return self.combo_reason.currentText()