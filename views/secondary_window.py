from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QHeaderView
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import os
import openpyxl


class SecondaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ventana Secundaria")
        self.setGeometry(100, 100, 1200, 600)

        # --- Widget central ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # --- Layout principal vertical ---
        main_layout = QVBoxLayout(main_widget)

        # --- Layout horizontal superior (inputs, labels, imagen) ---
        top_layout = QHBoxLayout()

        # --- Izquierda: Inputs y Labels ---
        left_layout = QVBoxLayout()

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("FUR CODE")
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Quantity")

        self.label_info1 = QLabel("Nombre: -")
        self.label_info2 = QLabel("Categoría: -")
        self.label_info3 = QLabel("Ubicación: -")

        self.button1 = QPushButton("Agregar")
        self.button2 = QPushButton("Restar")
        self.button1.clicked.connect(self.agregar_stock)
        self.button2.clicked.connect(self.restar_stock)

        self.excel_path = "src/rcklyt.xlsx"  # Ruta guardada para futuras actualizaciones


        for widget in [self.input1, self.input2, self.label_info1, self.label_info2, self.label_info3,
                       self.button1, self.button2]:
            left_layout.addWidget(widget)

        # --- Derecha: Imagen ---
        self.image_label = QLabel("Table Layout")
        self.image_label.setFixedSize(600, 250)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_layout.addLayout(left_layout)
        top_layout.addWidget(self.image_label)

        # --- Abajo: Tabla ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["FUR CODE", "STOCK", "TABLES IN USE"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

        # Agregar layouts al layout principal
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)

        self.load_inventory_data("src/rcklyt.xlsx")

    def load_inventory_data(self, file_path, sheet_name="Sheet1"):
        wb = openpyxl.load_workbook(file_path, data_only=True)
        if sheet_name not in wb.sheetnames:
            print(f"La hoja '{sheet_name}' no existe.")
            return

        ws = wb[sheet_name]
        self.table.setRowCount(0)

        # Leer encabezados
        headers = [cell.value for cell in ws[1]]  # Suponiendo que están en la fila 1
        try:
            idx_fur_code = headers.index("FUR CODE")
            idx_in_use = headers.index("IN USE")
            idx_stock = headers.index("STOCK")
        except ValueError as e:
            return

        for row in ws.iter_rows(min_row=2):  # Empieza desde la fila 2 (datos)
            fur_code = row[idx_fur_code].value
            in_use = row[idx_in_use].value
            stock = row[idx_stock].value

            # Solo añadir si hay FUR CODE (ignora filas vacías)
            if not fur_code:
                continue

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(fur_code)))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(stock)))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(in_use)))

        self.table.cellClicked.connect(self.on_cell_clicked)


# Nuevos métodos dentro de la clase:
    def agregar_stock(self):
        self.actualizar_stock(sumar=True)

    def restar_stock(self):
        self.actualizar_stock(sumar=False)

    def actualizar_stock(self, sumar=True):
        fur_code = self.input1.text().strip()
        cantidad_texto = self.input2.text().strip()

        if not fur_code or not cantidad_texto.isdigit():
            return  # Entradas inválidas

        cantidad = int(cantidad_texto)

        fila_encontrada = -1
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == fur_code:
                fila_encontrada = row
                break

        if fila_encontrada >= 0:
            # Ya existe, actualizar stock
            stock_item = self.table.item(fila_encontrada, 1)
            stock_actual = int(stock_item.text()) if stock_item else 0

            nuevo_stock = stock_actual + cantidad if sumar else stock_actual - cantidad
            nuevo_stock = max(nuevo_stock, 0)  # Evita números negativos

            self.table.setItem(fila_encontrada, 1, QTableWidgetItem(str(nuevo_stock)))
        else:
            # Si no existe, solo permitir agregar
            if sumar:
                nueva_fila = self.table.rowCount()
                self.table.insertRow(nueva_fila)
                self.table.setItem(nueva_fila, 0, QTableWidgetItem(fur_code))
                self.table.setItem(nueva_fila, 1, QTableWidgetItem(str(cantidad)))
                self.table.setItem(nueva_fila, 2, QTableWidgetItem("0"))
            else:
                print("No se puede restar a un código inexistente.")
                return

        # Actualizar Excel
        self.actualizar_excel()

    def actualizar_excel(self):
        wb = openpyxl.load_workbook(self.excel_path)
        ws = wb.active  # Asegura usar la hoja correcta

        # Borrar contenido desde la fila 2 (mantener encabezados)
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            for cell in row:
                cell.value = None

        for row in range(self.table.rowCount()):
            fur_code = self.table.item(row, 0).text()
            stock = self.table.item(row, 1).text()
            in_use = self.table.item(row, 2).text()

            ws.cell(row=row+2, column=6, value=fur_code)  # Columna F
            ws.cell(row=row+2, column=8, value=stock)     # Columna H
            ws.cell(row=row+2, column=9, value=in_use)    # Columna I, si "IN USE" va ahí

        wb.save(self.excel_path)


    def on_cell_clicked(self, row, col):
        fur_code_item = self.table.item(row, 0)
        stock_item = self.table.item(row, 1)
        in_use_item = self.table.item(row, 2)

        if not fur_code_item:
            return

        fur_code = fur_code_item.text().strip()
        stock = stock_item.text() if stock_item else "-"
        in_use = in_use_item.text() if in_use_item else "-"

        self.label_info1.setText(f"Nombre: {fur_code}")
        self.label_info2.setText(f"Cantidad: {stock}")
        self.label_info3.setText(f"En uso: {in_use}")

        # Buscar imagen en src/img
        image_path = os.path.join("src", "table_layouts", f"{fur_code}.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText("Sin imagen disponible")
            self.image_label.setPixmap(QPixmap())  # Limpiar imagen previa si no se encuentra
