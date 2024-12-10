from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.task_widgets.task_display import TaskDisplay
from app.widgets.schedule_widgets.schedule_display import InputRectangleDisplay
from datetime import datetime
import math

class NotificationWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Notification Page")
        self.setFixedSize(900, 600)
        self.center()
        self.parent_window = parent

        self.db_handler = DatabaseHandler()
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        self.msg_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.msg_layout)
        self.dynamic_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.dynamic_layout)
        self.time_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.time_layout)
        
        self.schedule_label = QtWidgets.QLabel(self)
        self.schedule_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
            }
        """)
        self.msg_layout.addWidget(self.schedule_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.time_label = QtWidgets.QLabel(self)
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
            }
        """)
        self.time_layout.addWidget(self.time_label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_window)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        self.update_window()

    def update_window(self):
        current_time = datetime.now().time()
        time_format = "%H:%M:%S"
        formatted_time = current_time.strftime(time_format)
        current_schedule = self.db_handler.get_current_task(formatted_time)
        t1 = datetime.strptime(formatted_time, time_format)
        t2 = datetime.strptime(current_schedule[5], time_format)
        time_difference = t2 - t1
        total_seconds = time_difference.total_seconds()
        minutes = math.ceil((total_seconds % 3600) / 60)
        
        hour = int(formatted_time[:2])
        if hour < 12: 
            greeting = "Morning"
        elif hour < 18:
            greeting = "Afternoon"
        else:
            greeting = "Evening"
            
        schedule_title = f"Good {greeting}, your current focus is {current_schedule[2]}"
        
        new_widget = InputRectangleDisplay(input_data=current_schedule)

        if self.msg_layout.count() == 2:
            # Remove the existing widget
            old_widget = self.msg_layout.takeAt(1).widget()
            if old_widget is not new_widget:
                old_widget.deleteLater()
                self.msg_layout.addWidget(new_widget)
        else:
            self.msg_layout.addWidget(new_widget)
        
                
        category = self.db_handler.get_category_by_id(current_schedule[1])
            
        if total_seconds > 3600:
            hours = int(total_seconds // 3600)
            message = f"Your {category[0]} block will end in {hours} hours and {minutes} minutes"
        else:
            message = f"Your {category[0]} block will end in {minutes} minutes"

        self.schedule_label.setText(f"{schedule_title}")
        self.time_label.setText(
            f"{message}"
        )

    def center(self):
        qr = self.frameGeometry()
        rect = QtCore.QRect(0, 0, 2560, 1450)
        cp = rect.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
