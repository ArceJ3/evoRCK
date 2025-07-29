from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
import sys
from views.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)

    apply_stylesheet(app, theme='dark_teal.xml')

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
