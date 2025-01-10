from PyQt6 import QtWidgets, QtCore, QtGui

class ProjectDropdown(QtWidgets.QWidget):
    tagSaved = QtCore.pyqtSignal(str, QtGui.QColor)  # Signal for saved tag (name and color)

    def __init__(self, parent=None):
        super(ProjectDropdown, self).__init__(parent)
        
        self.setWindowFlags(QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        
        self.update_mask()
        
        self.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 5px;")

        button_style = """
            QPushButton {
                background-color: white;
                padding: 5px;
                border: 2px solid black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: lightgrey;
            }
        """
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Name Input
        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setPlaceholderText("Project Name")
        main_layout.addWidget(self.name_input)

        # Color Display and Hex Input
        color_layout = QtWidgets.QHBoxLayout()
        self.color_display = QtWidgets.QLabel(self)
        self.color_display.setFixedSize(30, 30)
        self.color_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.color_input = QtWidgets.QLineEdit("#000000", self)
        self.color_input.setMaximumWidth(130)

        color_layout.addWidget(self.color_display)
        color_layout.addWidget(self.color_input)
        main_layout.addLayout(color_layout)

        # Color Picker Grid
        self.color_grid = QtWidgets.QGridLayout()
        self.color_grid.setSpacing(5)
        self.colors = [
            "#FF0000", "#33FF57", "#5733FF", "#FFD700", "#FF33A8", "#33FFF3", "#FF8C00", "#8A2BE2"
        ]

        for i, color in enumerate(self.colors):
            color_button = QtWidgets.QPushButton(self)
            color_button.setFixedSize(30, 30)
            color_button.setStyleSheet(f"background-color: {color};")
            color_button.clicked.connect(lambda _, c=color: self.set_selected_color(c))
            self.color_grid.addWidget(color_button, i // 8, i % 8)

        main_layout.addLayout(self.color_grid)

        # Action Buttons
        action_layout = QtWidgets.QHBoxLayout()
        back_button = QtWidgets.QPushButton("Back", self)
        back_button.setStyleSheet(button_style)
        back_button.clicked.connect(self.close)

        save_button = QtWidgets.QPushButton("Save Tag", self)
        save_button.setStyleSheet(button_style)
        save_button.clicked.connect(self.save_tag)

        action_layout.addWidget(back_button)
        action_layout.addWidget(save_button)
        main_layout.addLayout(action_layout)

    def update_mask(self):
        radius = 10
        rect = QtCore.QRectF(self.rect())
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(mask)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_mask()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Rounded white background
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FFFFFF")))  # White background
        painter.setPen(QtGui.QPen(QtGui.QColor("#B0B0B0"), 2, QtCore.Qt.PenStyle.DotLine))  # No additional border
        painter.drawRoundedRect(rect, 10, 10)  # Adjust radius for consistent rounded corners

        painter.end()
        
    def set_selected_color(self, color_hex):
        self.color_display.setStyleSheet(f"background-color: {color_hex}; border: 1px solid black;")
        self.color_input.setText(color_hex)

    def save_tag(self):
        tag_name = self.name_input.text()
        tag_color = QtGui.QColor(self.color_input.text())
        self.tagSaved.emit(tag_name, tag_color)
        self.close()