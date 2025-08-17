from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox, QMessageBox
)

class CustomReasonDialog(QDialog):
    def __init__(self, modo: str, fur_code: str, cantidad: str):
        super().__init__()

        self.setWindowTitle("Add" if modo == "add" else "Subtract")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        label_fur = QLabel(f"FUR CODE: {fur_code}")
        label_cantidad = QLabel(f"Quantity: {cantidad}")
        label_info = QLabel("Please select a reason:")
        label_info.setStyleSheet("margin-top: 10px; font-weight: bold")

        self.combo_reason = QComboBox()
        self.combo_reason.addItem("--- Select a reason ---")
        if modo == "add":
            self.combo_reason.addItems(["PUR", "PROJECT"])
        elif modo == "substract":
            self.combo_reason.addItems(["MAINTENANCE", "SCHEDULED", "MIGRATION"])

        layout.addWidget(label_fur)
        layout.addWidget(label_cantidad)
        layout.addWidget(label_info)
        layout.addWidget(self.combo_reason)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        botones.accepted.connect(self.validar_y_aceptar)
        botones.rejected.connect(self.reject)

        layout.addWidget(botones)

    def validar_y_aceptar(self):
        if self.combo_reason.currentIndex() == 0:
            QMessageBox.warning(self, "Error", "invalid option.")
            return
        self.accept()

    def get_reason(self):
        return self.combo_reason.currentText()
