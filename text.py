from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create QLineEdit widgets
        self.line_edit1 = QLineEdit(self)
        self.line_edit2 = QLineEdit(self)

        # Set validators to allow only 2-digit numbers
        validator = QIntValidator(0, 99, self)
        self.line_edit1.setValidator(validator)
        self.line_edit2.setValidator(validator)

        # Set a maximum length of 2 characters for each line edit
        self.line_edit1.setMaxLength(2)
        self.line_edit2.setMaxLength(2)

        # Set a fixed width for the line edits
        self.line_edit1.setFixedWidth(40)  # Adjust as needed
        self.line_edit2.setFixedWidth(40)  # Adjust as needed

        # Center the text inside the line edits
        self.line_edit1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.line_edit2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a horizontal layout
        hbox = QHBoxLayout()
        hbox.addWidget(self.line_edit1)
        hbox.addWidget(self.line_edit2)

        # Set the layout for the window
        self.setLayout(hbox)

# Main code to run the application
app = QApplication([])
window = MyWindow()
window.show()
app.exec()
