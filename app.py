import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from MainWindow import Ui_MainWindow
from animated_toggle import AnimatedToggle

# Define a simple input dialog for adding tasks
class InputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)
        self.setWindowTitle("Enter Details")
        self.setModal(True)

        # Input fields
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Task Name Input
        self.task_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(QtWidgets.QLabel("Task Name:"))
        self.layout.addWidget(self.task_input)
        
        # Set Time box
        self.time_layout = QtWidgets.QHBoxLayout()
        
        self.time_layout.addWidget(QtWidgets.QLabel("Select Start Time:"))
        self.start_time_layout = QtWidgets.QHBoxLayout()
        self.colon_label = QtWidgets.QLabel(':')
        self.colon_label.setFixedSize(10, 30)
        self.colon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_hr = QtWidgets.QLineEdit(self)
        self.start_min = QtWidgets.QLineEdit(self)
        validator = QtGui.QIntValidator(0, 99, self)
        self.start_hr.setValidator(validator)
        self.start_min.setValidator(validator)
        self.start_hr.setMaxLength(2)
        self.start_min.setMaxLength(2)
        self.start_hr.setFixedWidth(40)
        self.start_min.setFixedWidth(40)
        self.start_hr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_min.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_hr.setValidator(validator)
        self.start_min.setValidator(validator)
        self.start_time_layout.addWidget(self.start_hr)
        self.start_time_layout.addWidget(self.colon_label)
        self.start_time_layout.addWidget(self.start_min)

        self.vbox_1 = QtWidgets.QVBoxLayout()
        self.vbox_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_1.addLayout(self.start_time_layout)
        self.time_layout.addLayout(self.vbox_1)

        self.time_layout.addWidget(QtWidgets.QLabel("Select End Time:"))
        self.colon_label = QtWidgets.QLabel(':')
        self.colon_label.setFixedSize(10, 30)
        self.colon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_time_layout = QtWidgets.QHBoxLayout()
        self.end_hr = QtWidgets.QLineEdit(self)
        self.end_min = QtWidgets.QLineEdit(self)
        self.end_hr.setValidator(validator)
        self.end_min.setValidator(validator)
        self.end_hr.setMaxLength(2)
        self.end_min.setMaxLength(2)
        self.end_hr.setFixedWidth(40)
        self.end_min.setFixedWidth(40)
        self.end_hr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_min.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_hr.setValidator(validator)
        self.end_min.setValidator(validator)
        self.end_time_layout.addWidget(self.end_hr)
        self.end_time_layout.addWidget(self.colon_label)
        self.end_time_layout.addWidget(self.end_min)

        self.vbox_2 = QtWidgets.QVBoxLayout()
        self.vbox_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vbox_2.addLayout(self.end_time_layout)
        self.time_layout.addLayout(self.vbox_2)

        # Labels box
        self.label_layout = QtWidgets.QHBoxLayout()
        self.category_button = QtWidgets.QComboBox(self)
        self.category_button.setPlaceholderText("Category")
        self.category_button.addItems(["Work", "Leisure", "Routine"])
        self.repeatable_toggle = AnimatedToggle(self)
        self.repeatable_toggle.setFixedSize(self.repeatable_toggle.sizeHint())
        self.repeatable_toggle.setCheckable(True)
        self.label_layout.addWidget(self.category_button)
        self.label_layout.addWidget(self.repeatable_toggle)
        self.label_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # Button box
        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("Add Task", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.layout.addLayout(self.time_layout)
        self.layout.addLayout(self.label_layout)
        self.layout.addLayout(self.button_layout)
        
        # Set the dialog layout
        self.setLayout(self.layout)
        
    def get_input(self):
        toggle_state = self.repeatable_toggle.isChecked()
        return [self.task_input.text(), self.category_button.currentText(), str(toggle_state), 
                self.start_hr.text(), self.start_min.text(), self.end_hr.text(), self.end_min.text()]
    
    def on_ok(self):
        task_name = self.task_input.text()
        start_hour = self.start_hr.text()
        start_minute = self.start_min.text()
        end_hour = self.end_hr.text()
        end_min = self.end_min.text()
        category = self.category_button.currentText()
        if task_name and start_hour and start_minute and end_hour and end_min and category:
            print(f"Task Name: {category}")
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")

    def on_cancel(self):
        self.reject()
    
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Today's Tasks")

        self.pushButton.clicked.connect(self.open_input_dialog)
        self.center()

    def open_input_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec():  # If the user presses OK
            input_text = dialog.get_input()[2]
            self.add_new_block(input_text)

    def add_new_block(self, text):
        new_widget = QtWidgets.QLabel(text, self.centralwidget)
        self.verticalLayout.addWidget(new_widget)
        
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
