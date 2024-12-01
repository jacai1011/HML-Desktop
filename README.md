Requirements List
- Database to store items
- Desktop interface and UI
- Desktop interactivity with items
- Capability to track external app usage (ext: block websites)
- Day overview
- Instead of specifying work tasks cycle through a list throughout the day (add dropdown menu to choose task)


Systems
- RDBMS -> SQLite
- Workstation –> WSL2
- Workflow Mgmt -> Github
- Backend -> Python
- GUI -> PyQt6

Libraries
- Desktop UI
    - PyQt

Database Schema

Tasks
- taskID
- categoryID
- notificationID
- title
- dueDate
- description

Categories
- categoryID
- category

Notifications
- notificationID
- audio

