from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
import sys
from views.main_window import MainWindow  # Asegúrate de tener este import

def main():
    app = QApplication(sys.argv)

    apply_stylesheet(app, theme='dark_teal.xml')  # ✅ Aplica tema material

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
