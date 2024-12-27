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

Maybe needed to run:
- export DISPLAY=$(grep -oP '(?<=nameserver\s).+' /etc/resolv.conf):0
- export QT_QPA_PLATFORM=xcb
- export QT_XCB_GL_INTEGRATION=none

Todo
- add button that links to schedule list overview for each page
- add auto break timer for productivity
- cleanup ui for schedule input
- use QStackedWidget to avoid jarring page transition
- color theory
- make schedule input box taller
- During break show completed tasks
- change available project colors to less bright colors
- task window warnings background must be manually set as currently transparent=black