from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.task_widgets.task_display import TaskDisplay
import sys

class NotificationWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Notification Page")
        self.showFullScreen()