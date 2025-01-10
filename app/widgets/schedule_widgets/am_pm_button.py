from PyQt6 import QtWidgets, QtCore, QtGui
import sys

class AmPmButtonWidget(QtWidgets.QWidget):
    time_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(AmPmButtonWidget, self).__init__(parent)

        self.am_button = QtWidgets.QPushButton("AM", self)
        self.am_button.setCheckable(True)
        self.pm_button = QtWidgets.QPushButton("PM", self)
        self.pm_button.setCheckable(True)
        button_style = """
            QPushButton {
                background-color: white;
                padding: 5px;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: darkgray;
                border-style: inset;
            }
        """
        self.am_button.setStyleSheet(button_style)
        self.pm_button.setStyleSheet(button_style)

        self.am_button.clicked.connect(self.select_am)
        self.pm_button.clicked.connect(self.select_pm)
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.am_button)
        layout.addWidget(self.pm_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def select_am(self):
        self.pm_button.setStyleSheet("background-color: white;")
        self.am_button.setStyleSheet("background-color: lightblue;")
        self.pm_button.setChecked(False)
        self.time_selected.emit("AM")

    def select_pm(self):
        self.am_button.setStyleSheet("background-color: white;")
        self.pm_button.setStyleSheet("background-color: lightblue;")
        self.am_button.setChecked(False)
        self.time_selected.emit("PM")

    def sizeHint(self):
        return QtCore.QSize(130, 40)