from PyQt6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QIcon, QPixmap
from CustomInputDialog import InputDialog
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

        self.setLayout(self.layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Rectangle
        rect = self.rect().adjusted(5, 5, -5, -5)

        # Fill
        painter.setBrush(QBrush(Qt.GlobalColor.lightGray, Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine))

        # Corner
        corner_radius = 7
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

        # Text
        painter.setPen(QPen(Qt.GlobalColor.black))
        font = QFont("Arial", 16)
        painter.setFont(font)

        if self.data_submitted:
            # Time
            painter.drawText(rect, Qt.AlignmentFlag.AlignLeft, f"Category: {self.input_data[1]}")
            
            # Category Color
            
            # Resize based on Time taken

    def update_display(self, input_data):
        self.input_data = input_data
        self.data_submitted = True
        self.update()
        
        # Delete Button
        self.delete_button = QPushButton(self)
        self.delete_button.clicked.connect(self.on_delete)
        icon = QIcon(QPixmap("Transparent_X.png"))
        self.delete_button.setIcon(icon)
        self.delete_button.setIconSize(QSize(30, 30))
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        self.layout.addWidget(self.delete_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        # 
        
        self.layout.setContentsMargins(20, 20, 20, 20)
        
    def on_delete(self):
        self.close()
