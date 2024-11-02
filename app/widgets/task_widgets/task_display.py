from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from app.widgets.task_widgets.task_input import InputDialog
from db.db_handler import DatabaseHandler
from datetime import datetime, timedelta
import sys

class InputRectangleDisplay(QWidget):
    reposition_request = pyqtSignal(QWidget, int)
    def __init__(self, input_data=None):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.data_submitted = False
        self.setFixedHeight(270)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)
        
        self.time_label = QLabel("Placeholder")

        # Set layouts, whether or not input_data is provided
        self.top_layout = QHBoxLayout()
        self.middle_layout = QHBoxLayout()
        self.setLayout(self.layout)

        if input_data:
            self.input_data = input_data
            self.data_submitted = True
            self.update_display(input_data)
        else:
            self.input_dialog = InputDialog(self)
            self.input_dialog.submitted.connect(self.update_display)
            self.input_dialog.canceled.connect(self.close)
            self.layout.addWidget(self.input_dialog)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle Margins
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background Color
        if self.data_submitted:
            category = self.input_data[1]
            if category == 1:
                background_color = QColor(255, 99, 71)  # Tomato red for Work
            elif category == 2:
                background_color = QColor(135, 206, 235)  # Sky blue for Leisure
            elif category == 3:
                background_color = QColor(144, 238, 144)  # Light green for Routine
            elif category == 4:
                background_color = QColor(238, 130, 238)  # Violet for Self-Work
            else:
                background_color = Qt.GlobalColor.lightGray  # Default color
        else:
            background_color = Qt.GlobalColor.lightGray

        # Fill rectangle with chosen background color
        painter.setBrush(QBrush(background_color, Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        # Corner
        corner_radius = 7
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

        # Text
        painter.setPen(QPen(Qt.GlobalColor.black))
        font = QFont("Arial", 16)
        painter.setFont(font)

    def update_display(self, input_data):
        self.input_data = input_data
        self.data_submitted = True
        self.update()
        

        # Delete Button
        self.delete_button = QPushButton(self)
        self.delete_button.clicked.connect(self.on_delete)
        icon = QIcon(QPixmap("icons/Transparent_X.png"))
        self.delete_button.setIcon(icon)
        self.delete_button.setIconSize(QSize(30, 30))
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Activity Start Time
        start_12hr = self.input_data[4]
        time_obj = datetime.strptime(start_12hr, "%H:%M:%S")
        time_12hr = time_obj.strftime("%I:%M %p")
        end_12hr = self.input_data[5]
        time_obj_end = datetime.strptime(end_12hr, "%H:%M:%S")
        end_time_12hr = time_obj_end.strftime("%I:%M %p")
        self.time_label = QLabel(f"{time_12hr} - {end_time_12hr}")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align the text to the left
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)
        self.top_layout.addWidget(self.time_label)
        self.top_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.top_layout.setContentsMargins(10, 20, 10, 0)
        self.layout.addLayout(self.top_layout)
        
        # Activity Title
        title = self.input_data[2]
        title_label = QLabel(f"{title}")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
            }
        """)
        self.middle_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.middle_layout.setContentsMargins(10, 0, 10, 0)
        self.layout.addLayout(self.middle_layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        time_parts = list(map(int, self.input_data[6].split(':')))
        duration = timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])
        hrs = round(duration.total_seconds() / 3600)
        if hrs == 0:
            self.top_layout.setContentsMargins(10, 10, 10, 0)
            height = 100
        else:
            height = hrs * 150
        
        self.setFixedHeight(height)

        position = self.db_handler.get_position(self.input_data[0])
        self.request_reposition(position)
        
    def on_delete(self):
        self.db_handler.delete_task(self.input_data[0])
        output = self.db_handler.get_all_tasks()
        print(output)
        self.close()
    
    def get_start_time(self):
        return self.time_label.text()

    def request_reposition(self, position):
        self.reposition_request.emit(self, position[0]-1)