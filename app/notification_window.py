from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QMainWindow, QScrollArea, QSpacerItem
from PyQt6.QtCore import Qt, QTimer, QRect
from db.db_handler import DatabaseHandler
from app.widgets.notif_widgets.project_display import ProjectDisplay
from app.widgets.notif_widgets.notif_display import NotifDisplay
# from win11toast import notify

from datetime import datetime
import math

class NotificationWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Notification Page")
        self.setFixedSize(1100, 800)
        self.center()
        self.parent_window = parent

        self.db_handler = DatabaseHandler()
        self.update = False
        
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        layout = QVBoxLayout(self.centralwidget)
        
        self.msg_layout = QVBoxLayout()
        layout.addLayout(self.msg_layout)
        spacer = QSpacerItem(20, 50)
        layout.addItem(spacer)
        self.dynamic_layout = QVBoxLayout()
        layout.addLayout(self.dynamic_layout)
        self.time_layout = QVBoxLayout()
        layout.addLayout(self.time_layout)
        self.button_layout = QHBoxLayout()
        layout.addLayout(self.button_layout)
        
        self.msg_layout.setContentsMargins(0, 30, 0, 0)
        self.msg_layout.setSpacing(20)
        
        self.button_layout.setContentsMargins(0, 0, 30, 30)

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
        self.schedule_label = QLabel(self)
        self.schedule_label.setStyleSheet("""
            QLabel {
                font-size: 50px;
            }
        """)
        self.msg_layout.addWidget(self.schedule_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
            }
        """)
        self.time_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.backButton = QPushButton("Schedules", self.centralwidget)
        self.backButton.setStyleSheet(button_style)
        self.backButton.clicked.connect(self.open_schedule_list)
        
        self.button_layout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.update_window()
        self.set_background_image()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_window)
        self.timer.start(1000)
        
    def update_window(self):
        current_time = datetime.now().time()
        time_format = "%H:%M:%S"
        formatted_time = current_time.strftime(time_format)
        self.current_schedule = self.db_handler.get_current_schedule(formatted_time)
        t1 = datetime.strptime(formatted_time, time_format)
        t2 = datetime.strptime(self.current_schedule[5], time_format)
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
            
        schedule_title = f"Good {greeting}, your current schedule is"
        
        new_widget = NotifDisplay(input_data=self.current_schedule)

        if self.msg_layout.count() == 2:
            old_widget = self.msg_layout.itemAt(1).widget()
            if old_widget.get_name() != new_widget.get_name():
                old_widget = self.msg_layout.takeAt(1).widget()
                old_widget.deleteLater()
                if self.category[0] == "Productivity":
                    self.clear_layout(self.project_layout)
                self.msg_layout.addWidget(new_widget)
                self.show_system_notification(self.current_schedule[2])
                self.clear_layout(self.dynamic_layout)
                self.update = True
            else:
                self.update = False
        else:
            self.msg_layout.addWidget(new_widget)
            self.update = True

        self.category = self.db_handler.get_category_by_id(self.current_schedule[1])
        
        if self.category[0] == "Productivity" and self.update == True:
            self.msg_layout.setContentsMargins(0, 30, 0, 10)
            self.time_layout.setContentsMargins(0, 30, 0, 50)
            for i in reversed(range(self.dynamic_layout.count())):
                widget = self.dynamic_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.project_layout = QHBoxLayout()

            # Project Current Label
            self.project_current = QLabel(self)
            self.project_current.setStyleSheet("""
                QLabel {
                    font-size: 40px;
                }
            """)
            self.project_current.setText("Current Project:")
            self.project_layout.addWidget(self.project_current)

            self.project_dropdown = QComboBox(self)
            self.project_dropdown.setPlaceholderText("...")
            self.projects = self.db_handler.get_all_projects_by_category(self.current_schedule[1])
            self.project_dropdown.addItems([item[1] for item in self.projects])
            font_metrics = self.project_dropdown.fontMetrics()
            max_width = max(font_metrics.boundingRect(self.project_dropdown.itemText(i)).width()
                            for i in range(self.project_dropdown.count()))
            self.project_dropdown.setFixedWidth(max_width + 40)
            self.project_dropdown.currentTextChanged.connect(self.display_projects)
            self.project_layout.addWidget(self.project_dropdown)

            self.project_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dynamic_layout.addLayout(self.project_layout)

            self.scrollArea = QScrollArea(self.centralWidget())
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setFixedHeight(110)

            self.scrollAreaWidgetContents = QWidget()
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)

            self.scroll_layout = QVBoxLayout(self.scrollAreaWidgetContents)
            self.scrollAreaWidgetContents.setLayout(self.scroll_layout)

            self.dynamic_layout.addWidget(self.scrollArea)

            self.dynamic_layout.addStretch()
                        
        if total_seconds > 3600:
            hours = int(total_seconds // 3600)
            message = f"Your {self.category[0]} block will end in {hours} hours and {minutes} minutes"
        else:
            message = f"Your {self.category[0]} block will end in {minutes} minutes"

        self.schedule_label.setText(f"{schedule_title}")
        self.time_label.setText(
            f"{message}"
        )

    def open_schedule_list(self):
        self.timer.stop()
        self.parent_window.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        rect = QRect(0, 0, 2560, 1450)
        cp = rect.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_projects(self, current_project):
        project_id = self.db_handler.get_project_id(current_project)
        print(project_id)
        self.clear_layout(self.scroll_layout)
        widgets = self.db_handler.get_task_by_project_and_category(self.current_schedule[1], project_id[0])
        for widget in widgets:
            task = ProjectDisplay(input_data=widget)
            self.scroll_layout.addWidget(task)

    def clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def set_background_image(self):
        self.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
    def show_system_notification(self, schedule_title):
        msg = f"{schedule_title}"
        # notify('Next Schedule Reminder', msg)
