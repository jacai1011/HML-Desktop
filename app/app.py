import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from app.widgets.task_widgets.schedule_display import InputRectangleDisplay
from db.db_handler import DatabaseHandler
from app.task_list import TaskList
from app.widgets.center_widget import center


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.showFullScreen()
        self.setWindowTitle("Today's Schedule")

        self.db_handler = DatabaseHandler()
        self.db_handler.init_database()
        self.db_handler.insert_categories()
        

        # Central widget and main layout
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Create a vertical layout to hold the plus button, scroll area, and next button
        self.verticalLayout = QtWidgets.QVBoxLayout()

        # Plus button - lean left
        self.pushButton = QtWidgets.QPushButton("Add Task", self.centralwidget)
        self.pushButton.setIcon(QtGui.QIcon("icons/Plus_symbol.svg.png"))
        self.pushButton.setIconSize(QtCore.QSize(64, 64))
        self.pushButton.clicked.connect(self.add_new_block)  # Connect the add button to add_new_block method

        # Add plus button to the vertical layout and align left
        self.verticalLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        # Scroll area and its contents
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)  # Ensure resizable behavior
        self.scrollArea.setFixedSize(1200, 1100)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Add the scroll area to the vertical layout
        self.verticalLayout.addWidget(self.scrollArea)

        # Next button - lean right
        self.pushButton_2 = QtWidgets.QPushButton("Next", self.centralwidget)
        self.pushButton_2.setFixedSize(131, 61) 
        self.pushButton_2.clicked.connect(self.open_task_list_window)

        # Add next button to the vertical layout and align right
        self.verticalLayout.addWidget(self.pushButton_2, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.mainLayout.addLayout(self.verticalLayout)
        self.set_background_image()
        # Load saved tasks from the database
        self.input_data = self.db_handler.load_tasks()
        for entry in self.input_data:
            self.load_saved_tasks(entry)

    def add_new_block(self):
        """Add a new input block dynamically."""
        new_widget = InputRectangleDisplay()
        self.scroll_layout.insertWidget(0, new_widget)
        new_widget.reposition_request.connect(self.reposition_widget)

    def load_saved_tasks(self, input_data):
        """Load tasks from the database into the scroll area."""
        new_widget = InputRectangleDisplay(input_data=input_data)
        self.scroll_layout.addWidget(new_widget)

    def reposition_widget(self, widget, new_position):
        """Reposition an existing widget."""
        self.scroll_layout.removeWidget(widget)
        self.scroll_layout.insertWidget(new_position, widget)

    def open_task_list_window(self):
        """Open the task list window and close the current one."""
        self.secondary_window = TaskList()
        self.secondary_window.show()
        self.close()

    def set_background_image(self):
        # Set background image for the window using stylesheets
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
                border: none;  /* Remove the border of the scrollbar */
                background: transparent;  /* Make scrollbar background transparent */
                width: 0px;  /* Hide vertical scrollbar */
                height: 0px;  /* Hide horizontal scrollbar */
            }
            InputRectangleDisplay QPushButton {
                background-color: white;
                border: 1px solid #000;
                color: black;
            }
            InputRectangleDisplay QComboBox {
                background-color: white;
                border: 1px solid #000;
                color: black;
            }
            InputRectangleDisplay QLineEdit {
                background-color: white;
                border: 1px solid #000;
                color: black;
            }
        """)


# Run the application
app = QtWidgets.QApplication(sys.argv)
font = QtGui.QFont("Arial", 16)
app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())
