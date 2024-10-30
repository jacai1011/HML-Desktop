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
        
        # Add timeline sidebar
        
        # Add go next button
        
        # Reorder blocks based on time

    def add_new_block(self):
        new_widget = InputRectangleDisplay()
        self.scroll_layout.addWidget(new_widget)
        # category_id = self.db_handler.get_category_id(input_data[1])
        # self.db_handler.insert_task(input_data[0], category_id, input_data[2], input_data[3], input_data[4], input_data[5])
    
    # load saved tasks
        
    def center(self):
        qr = self.frameGeometry()
        rect = QtCore.QRect(0, 0, 2560, 1450)
        cp = rect.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
app = QtWidgets.QApplication(sys.argv)
font = QtGui.QFont("Arial", 16)
app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())
