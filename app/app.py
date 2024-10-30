import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from app.ui.MainWindow_ui import Ui_MainWindow
from app.widgets.task_widgets.task_display import InputRectangleDisplay
    
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Today's Schedule")

        self.scroll_layout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.pushButton.clicked.connect(self.add_new_block)
        self.center()
        
        # Add timeline sidebar
        
        # Add go next button
        
        # Reorder blocks based on time

    def add_new_block(self, input_data):
        new_widget = InputRectangleDisplay(input_data)
        self.scroll_layout.addWidget(new_widget)
        
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
