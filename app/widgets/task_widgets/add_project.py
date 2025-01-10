from PyQt6 import QtWidgets, QtCore, QtGui
from app.widgets.task_widgets.project_dropdown import ProjectDropdown
from db.db_handler import DatabaseHandler

class AddProject(QtWidgets.QPushButton):
    update_screen = QtCore.pyqtSignal()
    def __init__(self, text="Click Me", category_id=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.category = category_id
        self.db_handler = DatabaseHandler()
        self.font = QtGui.QFont("Arial", 16)
        self.font_metrics = QtGui.QFontMetrics(self.font)
        self.setFixedHeight(self.font_metrics.height() + 15)
        text_width = self.font_metrics.horizontalAdvance(text)
        self.setFixedWidth(text_width + 20)

        # Define colors
        self.background_color = QtGui.QColor("#FFFFFF")  # White background
        self.border_color = QtGui.QColor("#B0B0B0")  # Light gray border for blending
        self.border_hover_color = QtGui.QColor("#808080")  # Darker gray when hovering
        self.current_border_color = self.border_color

        # Enable hover tracking
        self.setMouseTracking(True)
        self.dropdown = None

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Button background
        rect = self.rect().adjusted(2, 2, -2, -2)  # Adjust to fit the border
        painter.setBrush(QtGui.QBrush(self.background_color))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 10, 10)  # Rounded corners

        # Dotted border
        border_pen = QtGui.QPen(self.current_border_color, 2, QtCore.Qt.PenStyle.DotLine)
        painter.setPen(border_pen)
        painter.drawRoundedRect(rect, 10, 10)

        # Button text
        painter.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.black))  # Text color
        painter.setFont(self.font)
        painter.drawText(rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.text())

        painter.end()

    def enterEvent(self, event):
        self.current_border_color = self.border_hover_color
        self.update()  # Trigger a repaint
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.current_border_color = self.border_color
        self.update()  # Trigger a repaint
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.dropdown:
            self.dropdown = ProjectDropdown(self)
            self.dropdown.tagSaved.connect(self.handle_tag_saved)

        dropdown_pos = self.mapToGlobal(self.rect().bottomLeft())
        self.dropdown.move(dropdown_pos)
        self.dropdown.show()

    def handle_tag_saved(self, name, color):
        self.db_handler.insert_project(name, color.name(), self.category)
        self.update_screen.emit()
        self.dropdown.hide()