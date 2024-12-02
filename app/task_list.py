from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.center_widget import center

class TaskList(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        self.showFullScreen()
        
