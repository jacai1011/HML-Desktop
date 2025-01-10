from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.task_widgets.task_display import TaskDisplay
from app.notification_window import NotificationWindow
import sys

class TaskList(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Task Page")
        self.showMaximized()
        self.parent_window = parent

        self.db_handler = DatabaseHandler()
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.mainLayout1 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mainLayout1.addLayout(self.mainLayout)
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout2 = QtWidgets.QVBoxLayout()

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
        
        self.pushButton = QtWidgets.QPushButton("Add Work Task", self.centralwidget)
        self.pushButton.setStyleSheet(button_style)
        self.pushButton.clicked.connect(self.add_new_work_task)

        self.verticalLayout1.addWidget(self.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumSize(800, 1100)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet("background: transparent;")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.verticalLayout1.addWidget(self.scrollArea)
        self.mainLayout.addLayout(self.verticalLayout1)

        self.pushButton1 = QtWidgets.QPushButton("Add Leisure Task", self.centralwidget)
        self.pushButton1.setStyleSheet(button_style)
        self.pushButton1.clicked.connect(self.add_new_leisure_task)

        self.verticalLayout2.addWidget(self.pushButton1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self.scrollArea1 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea1.setWidgetResizable(True)
        self.scrollArea1.setMaximumSize(800, 1100)

        self.scrollAreaWidgetContents1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents1.setStyleSheet("background: transparent;")
        self.scrollArea1.setWidget(self.scrollAreaWidgetContents1)
        self.scroll_layout1 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents1)
        self.scroll_layout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.verticalLayout2.addWidget(self.scrollArea1)
        
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.nextButton = QtWidgets.QPushButton("Start", self.centralwidget)
        self.nextButton.setStyleSheet(button_style)
        self.nextButton.setFixedSize(131, 61) 
        self.nextButton.clicked.connect(self.open_main_window)

        self.backButton = QtWidgets.QPushButton("Back", self.centralwidget)
        self.backButton.setStyleSheet(button_style)
        self.backButton.setFixedSize(131, 61) 
        self.backButton.clicked.connect(self.open_schedule_list)
        self.buttonLayout.addWidget(self.backButton)
        self.buttonLayout.addWidget(self.nextButton)
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setContentsMargins(0, 0, 450, 50)
        self.mainLayout.addLayout(self.verticalLayout2)
        self.mainLayout1.addLayout(self.buttonLayout)
        
        self.set_background_image()

        self.cat_id = self.db_handler.get_category_id("Productivity")
        self.input_data = self.db_handler.load_saved_tasks_by_project(self.cat_id[0])
        for entry in self.input_data:
            self.load_saved_work_tasks(entry)

        self.cat_id = self.db_handler.get_category_id("Leisure")
        self.input_data = self.db_handler.load_saved_tasks_by_project(self.cat_id[0])
        for entry in self.input_data:
            self.load_saved_leisure_tasks(entry)
            
    def set_background_image(self):
        self.setStyleSheet("""
            TaskList {
                background-image: url('icons/Capture.PNG');
            }
            
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea QScrollBar {
                border: none;
                background: transparent;
                width: 0px;
                height: 0px;
            }
        """)

    def add_new_work_task(self):
        self.cat_id = self.db_handler.get_category_id("Productivity")
        new_widget = TaskDisplay(input_data=None,category=self.cat_id[0])
        self.scroll_layout.addWidget(new_widget)

    def add_new_leisure_task(self):
        self.cat_id = self.db_handler.get_category_id("Leisure")
        new_widget = TaskDisplay(input_data=None,category=self.cat_id[0])
        self.scroll_layout1.addWidget(new_widget)

    def load_saved_work_tasks(self, input_data):
        self.cat_id = self.db_handler.get_category_id("Productivity")
        new_widget = TaskDisplay(input_data=input_data, category=self.cat_id[0])
        self.scroll_layout.addWidget(new_widget)

    def load_saved_leisure_tasks(self, input_data):
        self.cat_id = self.db_handler.get_category_id("Leisure")
        new_widget = TaskDisplay(input_data=input_data, category=self.cat_id[0])
        self.scroll_layout1.addWidget(new_widget)
    
    def open_schedule_list(self):
        self.parent_window.show()
        self.close()

    def open_main_window(self):
        self.main_window = NotificationWindow(self.parent_window)
        self.main_window.show()
        self.close()

app = QtWidgets.QApplication(sys.argv)
font = QtGui.QFont("Arial", 16)
app.setFont(font)

