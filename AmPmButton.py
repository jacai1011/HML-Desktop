from PyQt6 import QtWidgets, QtCore, QtGui
import sys

class AMPMButtonWidget(QtWidgets.QWidget):
    time_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(AMPMButtonWidget, self).__init__(parent)

        # Create AM and PM buttons
        self.am_button = QtWidgets.QPushButton("AM", self)
        self.pm_button = QtWidgets.QPushButton("PM", self)

        # Set default styles
        self.am_button.setStyleSheet("background-color: lightblue;")
        self.pm_button.setStyleSheet("background-color: white;")

        # Connect signals
        self.am_button.clicked.connect(self.select_am)
        self.pm_button.clicked.connect(self.select_pm)

        # Layout
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.am_button)
        layout.addWidget(self.pm_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def select_am(self):
        self.am_button.setStyleSheet("background-color: lightblue;")
        self.pm_button.setStyleSheet("background-color: white;")
        self.time_selected.emit("AM")

    def select_pm(self):
        self.am_button.setStyleSheet("background-color: white;")
        self.pm_button.setStyleSheet("background-color: lightblue;")
        self.time_selected.emit("PM")

    def sizeHint(self):
        return QtCore.QSize(100, 30)
