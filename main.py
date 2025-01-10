if __name__ == '__main__':

    # Set the attribute to disable high DPI scaling before QApplication is created
    import os
    os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0' 

    import sys
    from app import app
    # Run the app
    sys.exit(app.run())
