from PyQt6 import QtWidgets, QtCore, QtGui
from AnimatedToggle import AnimatedToggle
from AmPmButton import AMPMButtonWidget
import sys

class InputDialog(QtWidgets.QWidget):
    submitted = QtCore.pyqtSignal(list)
    canceled = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)

        self.am_pm_start_state = "AM" 
        self.am_pm_end_state = "AM"

        self.layout = QtWidgets.QVBoxLayout(self)

        # Activity Title
        self.task_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(QtWidgets.QLabel("Activity Title:"))
        self.layout.addWidget(self.task_input)
        
        # Time box
        self.time_layout = QtWidgets.QHBoxLayout()
        
        self.time_layout.addWidget(QtWidgets.QLabel("Start Time"))
        self.start_time_layout = QtWidgets.QHBoxLayout()
        self.start_time_layout.setContentsMargins(0, 0, 30, 0)
        self.colon_label = QtWidgets.QLabel(':')
        self.colon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.colon_label.setFixedSize(5, 30)
        self.start_hr = QtWidgets.QLineEdit(self)
        self.start_min = QtWidgets.QLineEdit(self)
        validator = QtGui.QIntValidator(0, 99, self)
        self.start_hr.setValidator(validator)
        self.start_min.setValidator(validator)
        self.start_hr.setMaxLength(2)
        self.start_min.setMaxLength(2)
        self.start_hr.setFixedWidth(40)
        self.start_min.setFixedWidth(40)
        self.am_pm_start = AMPMButtonWidget(self)
        self.am_pm_start.time_selected.connect(self.handle_start_state)
        self.am_pm_start.setFixedSize(self.am_pm_start.sizeHint())
        self.start_time_layout.addWidget(self.start_hr)
        self.start_time_layout.addWidget(self.colon_label)
        self.start_time_layout.addWidget(self.start_min)
        self.start_time_layout.addWidget(self.am_pm_start)
        self.time_layout.addLayout(self.start_time_layout)

        self.time_layout.addWidget(QtWidgets.QLabel("End Time"))
        self.end_time_layout = QtWidgets.QHBoxLayout()
        self.end_time_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.colon_label = QtWidgets.QLabel(':')
        self.colon_label.setFixedSize(5, 30)
        self.colon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_hr = QtWidgets.QLineEdit(self)
        self.end_min = QtWidgets.QLineEdit(self)
        self.end_hr.setValidator(validator)
        self.end_min.setValidator(validator)
        self.end_hr.setMaxLength(2)
        self.end_min.setMaxLength(2)
        self.end_hr.setFixedWidth(40)
        self.end_min.setFixedWidth(40)
        self.am_pm_end = AMPMButtonWidget(self)
        self.am_pm_end.time_selected.connect(self.handle_end_state)
        self.am_pm_end.setFixedSize(self.am_pm_end.sizeHint())
        self.end_time_layout.addWidget(self.end_hr)
        self.end_time_layout.addWidget(self.colon_label)
        self.end_time_layout.addWidget(self.end_min)
        self.end_time_layout.addWidget(self.am_pm_end)
        self.time_layout.addLayout(self.end_time_layout)

        # Labels box
        self.label_layout = QtWidgets.QHBoxLayout()
        self.category_button = QtWidgets.QComboBox(self)
        self.category_button.setPlaceholderText("Category")
        self.category_button.addItems(["Work", "Leisure", "Routine", "Self-Work"])
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
        
        self.layout.addSpacing(10)
        self.layout.addLayout(self.time_layout)

        self.layout.addLayout(self.label_layout)
        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)

    def get_input(self):
        return [self.task_input.text(), self.category_button.currentText(), str(self.repeatable_toggle.isChecked()), 
                self.start_hr.text(), self.start_min.text(), self.end_hr.text(), self.end_min.text(),
                self.am_pm_start_state, self.am_pm_end_state]
    
    def on_ok(self):
        task_name = self.task_input.text()
        start_hour = self.start_hr.text()
        start_minute = self.start_min.text()
        end_hour = self.end_hr.text()
        end_min = self.end_min.text()
        category = self.category_button.currentText()
        if start_hour and start_minute and end_hour and end_min and category:
            if (category == "Routine" and task_name) or (category != "Routine"):
                print(f"Task Name: {task_name}")
                input_data = self.get_input()
                self.submitted.emit(input_data)
                self.close()   # Optionally clear inputs after submission
            else:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Please add task name for Routine tasks.")
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all required fields.")

    def on_cancel(self):
        self.canceled.emit()
        self.close()
    
    def handle_start_state(self, selected):
        self.am_pm_start_state = selected
    
    def handle_end_state(self, selected):
        self.am_pm_end_state = selected
    