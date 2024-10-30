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
- task_id
- category_id
- title
- repeatable
- start_time
- end_time
- duration

Categories
- category_id
- category

Maybe needed to run:
export DISPLAY=$(grep -oP '(?<=nameserver\s).+' /etc/resolv.conf):0
export QT_QPA_PLATFORM=xcb
export QT_XCB_GL_INTEGRATION=none