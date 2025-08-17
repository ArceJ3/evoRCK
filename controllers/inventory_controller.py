# controllers/inventory_controller.py
import openpyxl
from PyQt6.QtWidgets import QMessageBox

class InventoryController:

    def load_inventory(file_path, sheet_name="Tables"):
        """Carga y agrupa datos del inventario desde Excel."""
        wb = openpyxl.load_workbook(file_path, data_only=True)
        if sheet_name not in wb.sheetnames:
            raise ValueError(f"La hoja '{sheet_name}' no existe en {file_path}")

        ws = wb[sheet_name]

        headers = [cell.value for cell in ws[1]]
        try:
            idx_table = headers.index("TABLE")        # A
            idx_zone = headers.index("ZONE")          # B
            idx_env = headers.index("ENVIRONMENT")    # C
            idx_id = headers.index("ID")              # D
            idx_fur_code = headers.index("FUR CODE")  # F
            idx_stock = headers.index("STOCK")        # H
        except ValueError as e:
            raise ValueError(f"Faltan columnas necesarias: {e}")

        # ---- Extraer todas las filas ----
        all_rows = []
        for row in ws.iter_rows(min_row=2):
            all_rows.append({
                "table": row[idx_table].value,
                "zone": row[idx_zone].value,
                "env": row[idx_env].value,
                "id": row[idx_id].value,
                "fur_code": row[idx_fur_code].value,
                "stock": row[idx_stock].value,
            })

        # ---- Agrupación por FUR CODE ----
        agrupado = {}
        for row in all_rows:
            fur_code = row["fur_code"]
            if not fur_code or fur_code in agrupado:
                continue

            coincidencias = [r for r in all_rows if r["id"] == fur_code]

            zonas = sorted({r["zone"] for r in coincidencias if r["zone"]})
            entornos = sorted({r["env"] for r in coincidencias if r["env"]})
            mesas = sorted({str(r["table"]) for r in coincidencias if r["table"]})

            stock = row["stock"] if isinstance(row["stock"], int) else 0

            agrupado[fur_code] = {
                "stock": stock,
                "zones": zonas,
                "envs": entornos,
                "tables": mesas
            }

        return agrupado


    def actualizar_excel(self, path, fur_code: str, cantidad: int, sumar: bool):
        wb = openpyxl.load_workbook(path)
        ws = wb.active
        # Buscar la fila donde está el FUR CODE
        for row in range(2, ws.max_row + 1):
            celda_fur = ws.cell(row=row, column=6)  # Columna F

            if celda_fur.value == fur_code:
                celda_stock = ws.cell(row=row, column=8)  # Columna H
                stock_actual = int(celda_stock.value) if celda_stock.value else 0

                nuevo_stock = stock_actual + cantidad if sumar else stock_actual - cantidad
                nuevo_stock = max(nuevo_stock, 0)  # Evita números negativos
                celda_stock.value = nuevo_stock
                break
        else:
            QMessageBox.warning(self, "Error", f"FUR CODE does not exist: {fur_code}")
            return

        wb.save(path)
        QMessageBox.information(self, "Éxito", f"Stock updated for: {fur_code}.")
