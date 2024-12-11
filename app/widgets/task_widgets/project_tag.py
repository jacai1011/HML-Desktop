from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
import sys

class ProjectTag(QtWidgets.QPushButton):  # Inherit from QPushButton

    def __init__(self, category_id=None, project_id=None, color=None, parent=None):
        super(ProjectTag, self).__init__(parent)
        
        self.category = category_id
        self.project = project_id
        self.color = color
        self.project_name = project_id

        # Set font and calculate text size
        self.font = QtGui.QFont("Arial", 16)
        self.font_metrics = QtGui.QFontMetrics(self.font)

        # Calculate the width needed for the text
        text_width = self.font_metrics.horizontalAdvance(self.project_name)
        self.setFixedHeight(self.font_metrics.height() + 20)

        # Calculate the widget width: text width + padding + space for delete button
        delete_button_width = 30  # Space for the delete button
        self.setFixedWidth(text_width + delete_button_width + 20)  # Add padding

        # Create layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 10, 0)

        # Add a label for the project name
        self.label = QtWidgets.QLabel(self.project_name, self)
        self.label.setStyleSheet("color: transparent;")
        self.label.setFont(self.font)
        self.layout.addWidget(self.label, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Add a delete button after the text
        self.delete_button = QtWidgets.QPushButton("X", self)
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                color: white;
                border-radius: 10px;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.layout.addWidget(self.delete_button)

        # Set overall style
        self.setStyleSheet("background-color: transparent; border: none;")
        self.delete_button.clicked.connect(self.handle_delete)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # Calculate the size of the text
        text_width = self.font_metrics.horizontalAdvance(self.project_name) + 20
        text_height = self.font_metrics.height()

        # Padding values
        horizontal_padding = 10
        vertical_padding = 5

        # Rectangle to fit the text with padding
        rect = QtCore.QRect(5, 5, text_width + 2 * horizontal_padding, text_height + 2 * vertical_padding)

        # Background Color
        background_color = QtGui.QColor(self.color)

        # Fill rectangle with chosen background color
        painter.setBrush(QtGui.QBrush(background_color, QtCore.Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QtGui.QPen(background_color, 3, QtCore.Qt.PenStyle.SolidLine))

        # Corner radius
        corner_radius = 7
        painter.drawRoundedRect(rect, corner_radius, corner_radius)

        # Draw the project name text
        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.white))  # Text color
        painter.setFont(self.font)

        # Adjust text rectangle to account for padding
        text_rect = rect.adjusted(horizontal_padding, vertical_padding, -horizontal_padding, -vertical_padding)
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignLeft, self.project_name)

        painter.end()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print(f"ProjectTag clicked: {self.project_name}")

    def handle_delete(self):
        print(f"Delete clicked for: {self.project_name}")