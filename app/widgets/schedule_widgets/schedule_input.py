from PyQt6 import QtWidgets, QtCore, QtGui
from app.widgets.schedule_widgets.animated_toggle import AnimatedToggle
from app.widgets.schedule_widgets.am_pm_button import AmPmButtonWidget
from datetime import datetime, time, timedelta
from db.db_handler import DatabaseHandler
import sys


class InputDialog(QtWidgets.QWidget):
    submitted = QtCore.pyqtSignal(list)
    canceled = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(InputDialog, self).__init__(parent)

        self.am_pm_start_state = "AM" 
        self.am_pm_end_state = "AM"
        
        font = QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold)
        self.setFont(font)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Activity Title
        self.task_input = QtWidgets.QLineEdit(self)
        line_style = """
            QLineEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
                font-size: 25px;
            }
        """
        self.task_input.setStyleSheet(line_style)
        self.layout.addWidget(QtWidgets.QLabel("Schedule Title:"))
        self.layout.addWidget(self.task_input)
        
        
        # Time box
        time_style = """
            QLineEdit {
                background-color: white;
                border: 2px solid black;
                border-radius: 5px;
                font-family: 'Roboto Mono', monospace;
                font-size: 30px;
            }
        """
        
        self.time_layout = QtWidgets.QHBoxLayout()
        self.time_layout.addWidget(QtWidgets.QLabel("Start Time"))
        self.start_time_layout = QtWidgets.QHBoxLayout()
        self.start_time_layout.setContentsMargins(0, 0, 30, 0)
        self.colon_label = QtWidgets.QLabel(':')
        self.colon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.colon_label.setFixedSize(5, 30)
        self.start_hr = QtWidgets.QLineEdit(self)
        self.start_hr.setStyleSheet(time_style)
        self.start_hr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_hr.setPlaceholderText("00")
        self.start_min = QtWidgets.QLineEdit(self)
        self.start_min.setStyleSheet(time_style)
        self.start_min.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_min.setPlaceholderText("00")
        validator = QtGui.QIntValidator(0, 12, self)
        self.start_hr.setValidator(validator)
        self.start_min.setValidator(validator)
        self.start_hr.setMaxLength(2)
        self.start_min.setMaxLength(2)

        font_metrics = self.start_hr.fontMetrics()
        char_width = font_metrics.boundingRect("0").width()
        padding = 20
        max_width = (char_width * self.start_hr.maxLength()) + padding
        
        self.start_hr.setFixedWidth(max_width)
        self.start_min.setFixedWidth(max_width)
        self.am_pm_start = AmPmButtonWidget(self)
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
        self.end_hr.setStyleSheet(time_style)
        self.end_hr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_hr.setPlaceholderText("00")
        self.end_min = QtWidgets.QLineEdit(self)
        self.end_min.setStyleSheet(time_style)
        self.end_min.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.end_min.setPlaceholderText("00")
        self.end_hr.setValidator(validator)
        self.end_min.setValidator(validator)
        self.end_hr.setMaxLength(2)
        self.end_min.setMaxLength(2)
        self.end_hr.setFixedWidth(max_width)
        self.end_min.setFixedWidth(max_width)

        self.am_pm_end = AmPmButtonWidget(self)
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
        self.category_button.addItems(["Work", "Leisure", "Routine", "Productivity"])
        self.category_button.setStyleSheet("""
            QComboBox {
                border: 2px solid black;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                font-size: 30px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(icons/drop_arrow.png);
                width: 14px;
                height: 14px;
            }
        """)
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
        button_style = """
            QPushButton {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: lightgrey;
            }
        """
        self.ok_button.setStyleSheet(button_style)
        self.cancel_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.layout.addSpacing(10)
        self.layout.addLayout(self.time_layout)

        self.layout.addLayout(self.label_layout)
        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)
        
    def on_ok(self):
        task_name = self.task_input.text()
        start_hour = self.handle_time_output(self.start_hr.text())
        start_minute = self.handle_time_output(self.start_min.text())
        end_hour = self.handle_time_output(self.end_hr.text())
        end_minute = self.handle_time_output(self.end_min.text())
        category = self.category_button.currentText()
        start_time = self.convert_24(start_hour, start_minute, self.am_pm_start_state)
        end_time = self.convert_24(end_hour, end_minute, self.am_pm_end_state)
        datetime1 = datetime.combine(datetime.today(), start_time)
        datetime2 = datetime.combine(datetime.today(), end_time)
        if datetime2 < datetime1:
            datetime2 += timedelta(days=1)
        time_difference = datetime2 - datetime1
        if category != '' and task_name:
            if time_difference.total_seconds() < 0:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Invalid length of time.")
            else:
                self.db_handler = DatabaseHandler()
                self.category_id = self.db_handler.get_category_id(category)[0]
                check_time = self.db_handler.check_timeslot_taken(start_time, end_time)
                if check_time[0] or check_time[1]:
                    QtWidgets.QMessageBox.warning(self, "Input Error", "Timeslot taken")
                else:
                    check = self.db_handler.insert_schedule(self.category_id, task_name, self.repeatable_toggle.isChecked(), start_time, end_time, time_difference)
                    if check:
                        QtWidgets.QMessageBox.warning(self, "Input Error", "Timeslot taken")
                    else:
                        output = self.db_handler.get_all_schedules()
                        print(output)
                        input_data = self.db_handler.get_all_schedules()[-1]
                        self.submitted.emit(input_data)
                        self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
            

    def on_cancel(self):
        self.canceled.emit()
        self.close()
    
    def handle_start_state(self, selected):
        self.am_pm_start_state = selected
    
    def handle_end_state(self, selected):
        self.am_pm_end_state = selected
        
    def handle_time_output(self, time):
        if time == '':
            return 0
        else:
            return int(time)
            
    def convert_24(self, hr, mi, ap):
        if ap == 'PM' and hr == 12:
            hr = 12
        elif ap == 'PM':
            hr = hr + 12
        elif ap == 'AM' and hr == 12:
            hr = hr - 12
        return time(hr, mi)
