import pytest
from PySide6.QtWidgets import QApplication, QPushButton
from pytestqt.qt_compat import qt_api

@pytest.mark.gui
def test_window_defaults(app_instance):
    window, state, controller = app_instance
    assert window._is_fullscreen
    assert not window._title_shown

@pytest.mark.gui
def test_button_click(app_instance, qtbot):
    """Test that clicking the push-to-talk button generates simulated ATC response."""
    window, state, controller = app_instance
    button = window.button_push_to_talk
    # 1. Simulate a mouse click on the button
    qtbot.mouseClick(button, qt_api.QtCore.Qt.MouseButton.LeftButton)
    # 2. Assert that simulated ATC response appeared
    #print(window.text_playbook.text()) # ToDo: to be captured by logs
    assert window.text_playbook.text() in state.playbook