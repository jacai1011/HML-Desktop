Requirements List
- Database to store items
- Desktop interface and UI
- Desktop interactivity with items
- Capability to track external app usage (ext: block websites)
- Day overview
- Instead of specifying work tasks cycle through a list throughout the day (add dropdown menu to choose task)


Systems
- RDBMS -> SQLite
- Linux System –> WSL
- Workflow Mgmt -> Github
- Backend -> Python
- Frontend -> PyQt5
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

Needed to run:
export DISPLAY=$(grep -oP '(?<=nameserver\s).+' /etc/resolv.conf):0
export QT_QPA_PLATFORM=xcb
export QT_XCB_GL_INTEGRATION=none