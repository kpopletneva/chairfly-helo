import sys
from PySide6 import QtWidgets
from ui_r22 import AppMainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Start full screen frameless
    window = AppMainWindow()
    window.resize_fullscreen_dimensions()
    window.enter_fullscreen()

    # Start the event loop
    sys.exit(app.exec())