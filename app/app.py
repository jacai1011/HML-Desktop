import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from app.ui.MainWindow_ui import Ui_MainWindow
from app.widgets.task_widgets.task_display import InputRectangleDisplay
from db.db_handler import DatabaseHandler
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Today's Schedule")
        
        self.db_handler = DatabaseHandler()
        self.db_handler.init_database()
        self.db_handler.insert_categories()

        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.pushButton.clicked.connect(self.add_new_block)
        self.center()
        
        self.input_data = self.db_handler.load_tasks()
        for entry in self.input_data:
            self.load_saved_tasks(entry)
        
        # Add timeline sidebar
        
        # Add go next button
        

    def add_new_block(self):
        new_widget = InputRectangleDisplay()
        self.scroll_layout.addWidget(new_widget)
        new_widget.reposition_request.connect(self.reposition_widget)

    def load_saved_tasks(self, input_data):
        new_widget = InputRectangleDisplay(input_data=input_data)
        self.scroll_layout.addWidget(new_widget)
        
    def center(self):
        qr = self.frameGeometry()
        rect = QtCore.QRect(0, 0, 2560, 1450)
        cp = rect.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reposition_widget(self, widget, new_position):
        self.scroll_layout.removeWidget(widget)
        self.scroll_layout.insertWidget(new_position, widget)
        
app = QtWidgets.QApplication(sys.argv)
font = QtGui.QFont("Arial", 16)
app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())
