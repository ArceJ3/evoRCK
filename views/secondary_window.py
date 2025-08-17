from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QHeaderView
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView
from PyQt6.QtWidgets import QMessageBox
from views.input_dialog import CustomReasonDialog
from controllers.inventory_controller import InventoryController as iv
from PyQt6.QtWidgets import QStyledItemDelegate

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

import os

class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EvoRCK")
        self.setGeometry(100, 100, 1200, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("FUR CODE")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Quantity")

        self.label_info1 = QLabel("<b>Name:</b> -")
        self.label_info2 = QLabel("<b>Category:</b> -")
        self.label_info3 = QLabel("<b>Location:</b> -")
        self.label_info4 = QLabel("<b>Envoronment:</b> -")

        self.button1 = QPushButton()
        self.button2 = QPushButton()

        icon_size = QSize(70, 70)

        self.button1.setIcon(QIcon("src/img/add.png"))
        self.button1.setIconSize(icon_size)
        self.button1.setFixedSize(icon_size)

        self.button2.setIcon(QIcon("src/img/substract.png"))
        self.button2.setIconSize(icon_size)
        self.button2.setFixedSize(icon_size)

        self.button1.clicked.connect(lambda: self.modificar_stock("add"))
        self.button2.clicked.connect(lambda: self.modificar_stock("substract"))

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        for widget in [self.input1, self.input2, self.label_info1, self.label_info2, self.label_info3, self.label_info4]:
            left_layout.addWidget(widget)

        left_layout.addLayout(button_layout)

        self.excel_path = "src/rcklyt.xlsx"  ### Ruta del archivo de

        self.image_label = QLabel("Table Layout")
        self.image_label.setFixedSize(600, 250)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout.addLayout(left_layout)
        top_layout.addWidget(self.image_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["FUR CODE", "STOCK", "ZONE", "ENVIRONMENT"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.table.horizontalHeader()

        # Ajuste de columnas:
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # FUR CODE
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # STOCK
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # ZONE
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # ENVIRONMENT

        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)  


        class CenterDelegate(QStyledItemDelegate):
            def initStyleOption(self, option, index):
                super().initStyleOption(option, index)
                option.displayAlignment = Qt.AlignmentFlag.AlignCenter

        self.table.setItemDelegate(CenterDelegate(self.table))
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        self.load_inventory_data()

    def load_inventory_data(self):
        try:
            self.data = iv.load_inventory(self.excel_path)
        except Exception as e:
            print(f"Error cargando inventario: {e}")
            return
        self.table.setRowCount(0)
        for fur_code, data in self.data.items():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(fur_code))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(data["stock"])))
            self.table.setItem(row_position, 2, QTableWidgetItem(" - ".join(data["zones"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(" - ".join(data["envs"])))
        self.table.cellClicked.connect(self.on_cell_clicked)

    
    def actualizar_stock(self, sumar=True):
        dialogo = CustomReasonDialog()
        if dialogo.exec():
            datos = dialogo.get_data()
            self.label_info1.setText(f"<b>Name:</b> {datos['nombre']}")
            self.label_info2.setText(f"<b>Category:</b> {datos['categoria']}")
            self.label_info3.setText(f"<b>Location:</b> {datos['ubicacion']}")
        fur_code = self.input1.text().strip()
        cantidad_texto = self.input2.text().strip()

        if not fur_code or not cantidad_texto.isdigit():
            return

        cantidad = int(cantidad_texto)

        fila_encontrada = -1
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == fur_code:
                fila_encontrada = row
                break

        if fila_encontrada >= 0:
            stock_item = self.table.item(fila_encontrada, 1)
            stock_actual = int(stock_item.text()) if stock_item else 0

            nuevo_stock = stock_actual + cantidad if sumar else stock_actual - cantidad
            nuevo_stock = max(nuevo_stock, 0)

            self.table.setItem(fila_encontrada, 1, QTableWidgetItem(str(nuevo_stock)))
        else:
            if sumar:
                nueva_fila = self.table.rowCount()
                self.table.insertRow(nueva_fila)
                self.table.setItem(nueva_fila, 0, QTableWidgetItem(fur_code))
                self.table.setItem(nueva_fila, 1, QTableWidgetItem(str(cantidad)))
                self.table.setItem(nueva_fila, 2, QTableWidgetItem("-"))
                self.table.setItem(nueva_fila, 3, QTableWidgetItem("-"))
            else:
                print("Cannot substract.")
                return

    def on_cell_clicked(self, row, col):
        fur_code_item = self.table.item(row, 0)
        if not fur_code_item:
            return

        fur_code = fur_code_item.text().strip()
        self.input1.setText(fur_code)
        data = self.data.get(fur_code, {})
        mesas = data.get("tables", [])
        zonas = data.get("zones", [])
        entornos = data.get("envs", [])

        self.label_info1.setText(f"<b>Name:</b> {fur_code}")
        self.label_info2.setWordWrap(True)
        self.label_info2.setText(f"<b>Tables:</b> ({len(mesas)}):\n{', '.join(mesas)}")
        self.label_info2.setMinimumHeight(40)
        self.label_info3.setWordWrap(True)
        self.label_info3.setText(f"<b>Zones:</b> {', '.join(zonas)}")
        self.label_info4.setWordWrap(True)
        self.label_info4.setText(f"<b>Environments:</b> {', '.join(entornos)}")

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
            self.image_label.setPixmap(QPixmap())

    def modificar_stock(self, modo: str):
        fur_code = self.input1.text().strip()
        cantidad_texto = self.input2.text().strip()
        if not fur_code or not cantidad_texto.isdigit():
            QMessageBox.warning(self, "Error", "You must use a valid FUR CODE or quantity.")
            return
        cantidad = int(cantidad_texto)
        dialogo = CustomReasonDialog(modo=modo, fur_code=fur_code, cantidad=cantidad)
        if dialogo.exec():
            razon = dialogo.get_reason()
            if not razon:
                QMessageBox.warning(self, "Error", "You must select a reason.")
                return
            mensaje = (f"Do you want to {modo.upper()}\n\nFUR CODE: {fur_code}\nQuantity: {cantidad}\nReason: {razon}\n")
            respuesta = QMessageBox.question(
                self,
                "Confirm",
                mensaje,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.razon_actual = razon
                self.actualizar_excel(
                    fur_code=fur_code,
                    cantidad=cantidad,
                    sumar=(modo == "add")
                )

    def actualizar_excel(self, fur_code: str, cantidad: int, sumar: bool):
        iv.actualizar_excel(self, self.excel_path, fur_code, cantidad, sumar)
        self.load_inventory_data()