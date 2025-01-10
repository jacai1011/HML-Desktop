from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from app.widgets.schedule_widgets.schedule_input import InputDialog
from db.db_handler import DatabaseHandler
from datetime import datetime, timedelta
import sys

class NotifDisplay(QWidget):
    def __init__(self, input_data=None):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.setFixedHeight(270)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)

        self.top_layout = QHBoxLayout()
        self.middle_layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.input_data = input_data
        
        # Activity Start Time
        start_12hr = self.input_data[4]
        time_obj = datetime.strptime(start_12hr, "%H:%M:%S")
        time_12hr = time_obj.strftime("%I:%M %p")
        end_12hr = self.input_data[5]
        time_obj_end = datetime.strptime(end_12hr, "%H:%M:%S")
        end_time_12hr = time_obj_end.strftime("%I:%M %p")
        self.time_label = QLabel(f"{time_12hr} - {end_time_12hr}")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)
        self.top_layout.addWidget(self.time_label)
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
        height = 150

        self.setFixedHeight(height)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle Margins
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background Color

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
    
    def get_name(self):
        return self.input_data[2]