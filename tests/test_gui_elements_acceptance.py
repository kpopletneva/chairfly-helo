import pytest
from PySide6.QtWidgets import QApplication, QPushButton
from pytestqt.qt_compat import qt_api

@pytest.mark.gui
def test_window_defaults(app_instance):
    window, state, controller = app_instance
    assert window._is_fullscreen
    assert not window._title_shown