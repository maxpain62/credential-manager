from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from backend.database import create_table
from PyQt6.QtGui import QGuiApplication


import sys

create_table()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())