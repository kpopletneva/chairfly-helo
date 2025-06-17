import sys
from PySide6 import QtWidgets
from models.state_manager import AppState
from views.ui_r22 import AppMainWindow
from controllers.app_controller import AppController

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Start full screen frameless
    state = AppState()
    window = AppMainWindow()
    controller = AppController(view=window, model=state)
    window.resize_fullscreen_dimensions()
    window.enter_fullscreen()

    # Start the event loop
    sys.exit(app.exec())