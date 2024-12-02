from PyQt6 import QtCore

def center(window):
    qr = window.frameGeometry()
    # Get screen geometry; adjust if you need a specific screen or resolution.
    screen_geometry = QtCore.QRect(0, 0, 2560, 1450)
    cp = screen_geometry.center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())
