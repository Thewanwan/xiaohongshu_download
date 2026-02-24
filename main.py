import sys
from PySide6.QtWidgets import QApplication
from app.ui.window import Win

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Win()
    w.show()
    sys.exit(app.exec())