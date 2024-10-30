from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from app.widgets.task_widgets.task_input import InputDialog
from db.db_handler import DatabaseHandler
from datetime import datetime, timedelta
import sys

class InputRectangleDisplay(QWidget):
    def __init__(self, input_data=None):
        super().__init__()
        self.data_submitted = False
        self.setFixedHeight(270)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.input_dialog = InputDialog(self)
        self.input_dialog.submitted.connect(self.update_display)  # Connect the signal to the slot
        self.input_dialog.canceled.connect(self.close)  # Connect the canceled signal to close the rectangle display
        self.layout.addWidget(self.input_dialog)  # Add the child widget to the layout

        self.top_layout = QHBoxLayout()
        self.middle_layout = QHBoxLayout()
        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle Margins
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background Color
        # todo: fix inputdata grab connecty to db
        if self.data_submitted:
            category = self.input_data[1]
            if category == "Work":
                background_color = QColor(255, 99, 71)  # Tomato red for Work
            elif category == "Leisure":
                background_color = QColor(135, 206, 235)  # Sky blue for Leisure
            elif category == "Routine":
                background_color = QColor(144, 238, 144)  # Light green for Routine
            elif category == "Self-Work":
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
        
        # self.db_handler = DatabaseHandler()
    
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
        time_label = QLabel(f"{time_12hr}")
        time_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align the text to the left
        time_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)
        self.top_layout.addWidget(time_label)
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
        
    def on_delete(self):
        self.close()
