import os
import pytest
from PySide6.QtWidgets import QApplication
from pytestqt.qt_compat import qt_api
from app.models.state_manager import AppState
from app.views.ui_r22 import AppMainWindow
from app.controllers.app_controller import AppController

# Force Qt into headless/offscreen mode (important for GitHub Actions CI)
os.environ["QT_QPA_PLATFORM"] = "offscreen"

@pytest.fixture
def app_instance(qtbot):
    """
    Fixture to create and manage the application instance for each test.
    """
    # Check if a QApplication instance already exists
    app = QApplication.instance()
    if not app:
        # If no instance exists, create a new one
        app = QApplication([])
    state = AppState()
    window = AppMainWindow()
    controller = AppController(view=window, model=state)
    window.resize_fullscreen_dimensions()
    window.enter_fullscreen()

    # Register the widget with the qtbot for testing
    qtbot.addWidget(window)

    return window, state, controller