from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from app.widgets.task_widgets.task_input import TaskInput
from db.db_handler import DatabaseHandler
from datetime import datetime, timedelta
import sys

class TaskDisplay(QWidget):

    def __init__(self, input_data=None, category=None):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.data_submitted = False
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 10, 20, 10)
        
        self.color = "#D3D3D3"

        self.top_layout = QHBoxLayout()
        self.setLayout(self.layout)

        if input_data:
            self.input_data = input_data
            self.data_submitted = True
            self.update_display(input_data)
        else:
            self.input_dialog = TaskInput(category_id=category, parent=self)
            self.input_dialog.submitted.connect(self.update_display)
            self.input_dialog.canceled.connect(self.close)
            self.layout.addWidget(self.input_dialog)
            
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle Margins
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Background Color
        background_color = QColor(self.color)

        # Fill rectangle with chosen background color
        painter.setBrush(QBrush(background_color, Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        # Corner
        corner_radius = 7
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

    def update_display(self, input_data):
        self.input_data = input_data
        self.data_submitted = True
        
        self.project_color = self.db_handler.get_project_color(self.input_data[3])
        if self.input_data[3] == 1:
            self.color = QColor(135, 206, 235)
        else:
            self.color = self.project_color[0]
        
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

        # Activity Title
        title = self.input_data[2]
        title_label = QLabel(f"{title}")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 35px;
            }
        """)
        self.top_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignTop)
        self.top_layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.top_layout.setContentsMargins(10, 20, 10, 0)
        self.layout.addLayout(self.top_layout)
        
        self.setFixedHeight(150)


    def on_delete(self):
        self.db_handler.delete_task(self.input_data[0])
        self.close()