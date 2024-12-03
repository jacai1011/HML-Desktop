from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.center_widget import center

class TaskList(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Window")
        self.showFullScreen()

        self.db_handler = DatabaseHandler()
        self.db_handler.init_database()
        self.db_handler.insert_categories()
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        
