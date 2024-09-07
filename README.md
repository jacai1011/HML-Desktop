Requirements List
- Database to store items
- Desktop interface and UI
- Desktop interactivity with items
- Capability to track external app usage

Systems
- RDBMS -> SQLite
- Linux System –> WSL
- Workflow Mgmt -> Github
- Backend -> Python
- Frontend -> Tkinter/Electron (JS)
- Integration -> Flask

Libraries
- Desktop UI (X)
    - Tkinter 
    - PyQt
- Tracking 
    - psutil

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