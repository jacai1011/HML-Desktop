from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from app.widgets.schedule_widgets.schedule_input import InputDialog
from db.db_handler import DatabaseHandler
from datetime import datetime, timedelta
import sys

class ProjectDisplay(QWidget):
    def __init__(self, input_data=None):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.input_data = input_data
        
        # Activity Title
        title = self.input_data[2]
        title_label = QLabel(f"{title}")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
            }
        """)

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
        
        complete_button = QPushButton("Done")
        complete_button.setStyleSheet(button_style)
        complete_button.setFixedWidth(170)
        complete_button.clicked.connect(self.complete_task)
        
        self.layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(complete_button)
        self.layout.setContentsMargins(20, 10, 20, 10)
        height = 100

        self.setFixedHeight(height)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle Margins
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background Color
        background_color = Qt.GlobalColor.lightGray

        # Fill rectangle with chosen background color
        painter.setBrush(QBrush(background_color, Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        # Corner
        corner_radius = 7
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

    
    def complete_task(self):
        self.db_handler.delete_task(self.input_data[0])
        self.close()