import sys
from PyQt6 import QtWidgets, QtCore, QtGui

from app.widgets.schedule_widgets.schedule_display import InputRectangleDisplay
from db.db_handler import DatabaseHandler
from app.task_list import TaskList
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Today's Schedule")
        self.resize(800, 600)
        self.showMaximized()

        self.db_handler = DatabaseHandler()
        self.db_handler.init_database()
        self.db_handler.insert_categories()
        cat_id = self.db_handler.get_category_id("Leisure")
        self.db_handler.insert_gaming_project_holder(cat_id[0])
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        button_style = """
            QPushButton {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: lightgrey;
            }
        """
        
        self.pushButton = QtWidgets.QPushButton("Add Schedule", self.centralwidget)
        self.pushButton.setStyleSheet(button_style)

        self.pushButton.clicked.connect(self.add_new_block)

        self.verticalLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumSize(1200, 1100)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.scrollArea)

        self.pushButton_2 = QtWidgets.QPushButton("Next", self.centralwidget)
        self.pushButton_2.setStyleSheet(button_style)
        self.pushButton_2.setFixedSize(131, 61) 
        self.pushButton_2.clicked.connect(self.open_task_list_window)

        self.verticalLayout.addWidget(self.pushButton_2, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.mainLayout.addLayout(self.verticalLayout)
        self.set_background_image()
        
        self.input_data = self.db_handler.load_schedules()
        for entry in self.input_data:
            self.load_saved_tasks(entry)

    def add_new_block(self):
        new_widget = InputRectangleDisplay()
        self.scroll_layout.insertWidget(0, new_widget)
        new_widget.reposition_request.connect(self.reposition_widget)

    def load_saved_tasks(self, input_data):
        new_widget = InputRectangleDisplay(input_data=input_data)
        self.scroll_layout.addWidget(new_widget)

    def reposition_widget(self, widget, new_position):
        self.scroll_layout.removeWidget(widget)
        print(new_position)
        self.scroll_layout.insertWidget(new_position, widget)

    def open_task_list_window(self):
        self.secondary_window = TaskList(self)
        self.secondary_window.show()
        self.close()

    def set_background_image(self):
        self.setStyleSheet("""
            MainWindow {
                background-image: url('icons/Capture.PNG');
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea QWidget {
                background: transparent;
            }
            QScrollArea QScrollBar {
                border: none;
                background: transparent;
                width: 0px;
                height: 0px;
            }
            InputRectangleDisplay QComboBox {
                background-color: white;
                border: 1px solid #000;
                color: black;
            }
        """)



app = QtWidgets.QApplication(sys.argv)
font = QtGui.QFont("Arial", 16)
app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())

# pyinstaller --noconsole --icon=app_icon.ico main.py + copy icons folder into main
