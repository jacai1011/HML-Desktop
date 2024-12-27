from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
import sys

class ProjectTag(QtWidgets.QPushButton):
    project_add = QtCore.pyqtSignal(int)

    def __init__(self, input_data=None, parent=None):
        super(ProjectTag, self).__init__(parent)
        
        self.db_handler = DatabaseHandler()
        self.id = input_data[0]
        self.color = input_data[2]
        self.project_name = input_data[1]
        self.hover = False
        self.repaint = False
        
        self.setCheckable(True)

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
        if self.hover == False:
            if self.isChecked() and self.repaint == False:
                widget_color = self.color
            else:
                widget_color = self.darken_color(self.color, 0.6)
        else:
            widget_color = self.darken_color(self.color, 0.8)
        
        background_color = QtGui.QColor(widget_color)

        # Fill rectangle with chosen background color
        painter.setBrush(QtGui.QBrush(background_color, QtCore.Qt.BrushStyle.SolidPattern))

        # Border
        painter.setPen(QtGui.QPen(background_color, 2, QtCore.Qt.PenStyle.SolidLine))

        # Corner radius
        corner_radius = 10
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
        self.hover = False
        if self.isChecked() and self.repaint == False:
            self.repaint = True
        elif self.repaint == True:
            self.repaint = False
        else:
            self.project_add.emit(self.id)
            
        self.update()

    def handle_delete(self):
        self.db_handler.delete_project(self.id)
        self.close()

    def enterEvent(self, event):
        self.hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover = False
        self.update()
        super().leaveEvent(event)

    def darken_color(self, hex_color, factor):
        hex_color = hex_color.lstrip('#')
        
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Convert back to hex and return
        return f"#{r:02x}{g:02x}{b:02x}"