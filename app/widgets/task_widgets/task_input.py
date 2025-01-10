from PyQt6 import QtWidgets, QtCore, QtGui
from db.db_handler import DatabaseHandler
from app.widgets.task_widgets.project_tag import ProjectTag
from app.widgets.task_widgets.add_project import AddProject
import sys

class TaskInput(QtWidgets.QWidget):
    submitted = QtCore.pyqtSignal(list)
    canceled = QtCore.pyqtSignal()
    def __init__(self, category_id=None, parent=None):
        super().__init__(parent)
        self.category = category_id
        self.db_handler = DatabaseHandler()
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.category_name = self.db_handler.get_category_by_id(self.category)
        
        font = QtGui.QFont("Arial", 14, QtGui.QFont.Weight.Bold)
        self.setFont(font)
        self.project_tag = None

        line_style = """
            QLineEdit {
                background-color: white;
                padding: 10px;
                border: 2px solid black;
                border-radius: 5px;
                font-size: 25px;
            }
        """
        # Activity Title
        self.task_input = QtWidgets.QLineEdit(self)
        self.task_input.setStyleSheet(line_style)
        self.layout.addWidget(QtWidgets.QLabel("Title:"))
        self.layout.addWidget(self.task_input)
        
        if self.category_name[0] == "Productivity":
        
            self.layout.addWidget(QtWidgets.QLabel("Project:"))
            
            self.project_layout = QtWidgets.QHBoxLayout()
            self.project_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

            self.button_group = QtWidgets.QButtonGroup(self)
            self.button_group.setExclusive(True)
            
            self.input_data = self.db_handler.get_all_projects_by_category(self.category)
            if self.input_data:
                for entry in self.input_data:
                    self.load_saved_projects(entry)

            self.add_project_button = AddProject("New Project", category_id=self.category)
            self.add_project_button.setStyleSheet(line_style)
            self.project_layout.addWidget(self.add_project_button)
            self.add_project_button.update_screen.connect(self.update_new_project)
                
            self.layout.addLayout(self.project_layout)

  

        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("Add Task", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
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
        self.ok_button.setStyleSheet(button_style)
        self.cancel_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)

    def on_cancel(self):
        self.canceled.emit()
        self.close()

    def on_ok(self):
        task_name = self.task_input.text()
        proj_category = self.category
        if self.category_name[0] == "Productivity":
            proj_id = self.project_tag
        else:
            proj_id = 1
        if task_name and proj_id and proj_category:
            check = self.db_handler.insert_task(proj_category, task_name, proj_id)
            if check:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Task Name taken")
            else:
                output = self.db_handler.get_all_tasks_by_category(proj_category)
                input_data = self.db_handler.get_all_tasks_by_category(proj_category)[-1]
                self.submitted.emit(input_data)
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
    
    def load_saved_projects(self, input_data):
        tag = ProjectTag(input_data=input_data)
        tag.project_add.connect(self.add_project)
        self.project_layout.addWidget(tag)
        self.button_group.addButton(tag)
        
    def update_new_project(self):
        tag_data = self.db_handler.get_new_project()
        tag = ProjectTag(input_data=tag_data)
        tag.project_add.connect(self.add_project)
        self.project_layout.insertWidget(self.project_layout.count() - 1, tag)
        self.button_group.addButton(tag)
    
    def add_project(self, tag_id):
        self.project_tag = tag_id