import sys, os
import pytest
from PySide6.QtWidgets import QApplication, QPushButton
from pytestqt.qt_compat import qt_api

#print("CWD:", os.getcwd())
#print("sys.path[0]:", sys.path[0])

@pytest.mark.gui
def test_window_defaults(app_instance):
    window, state, controller = app_instance
    assert window._is_fullscreen
    assert not window._title_shown