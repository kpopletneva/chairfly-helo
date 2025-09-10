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

@pytest.mark.gui
def test_toggle_button_collapses_frame_checklist(app_instance, qtbot):
    """Test that collapse '>>' and expand '<<' buttons works correctly for checklist frame."""
    window, state, controller = app_instance
    collapse_button = window.checklist_collapse_button
    expand_button = window.checklist_collapsed_bar

    # 1. Simulate click on the collapse button
    qtbot.mouseClick(collapse_button, qt_api.QtCore.Qt.LeftButton)
    # 2. Verify the collapsed bar is visible instead of the expanded one
    assert not window.frame_checklist.isVisible()
    assert window.checklist_collapsed_bar.isVisible()

    # 3. Simulate click on the expand button
    qtbot.mouseClick(expand_button, qt_api.QtCore.Qt.LeftButton)
    # 4. Verify the expanded bar is visible and collapsed is not
    assert window.frame_checklist.isVisible()
    assert not window.checklist_collapsed_bar.isVisible()

@pytest.mark.gui
def test_toggle_button_collapses_playbook_checklist(app_instance, qtbot):
    """Test that collapse '>>' and expand '<<' buttons works correctly for playbook frame."""
    window, state, controller = app_instance
    collapse_button = window.playbook_collapse_button
    expand_button = window.playbook_collapsed_bar

    # 1. Simulate click on the collapse button
    qtbot.mouseClick(collapse_button, qt_api.QtCore.Qt.LeftButton)
    # 2. Verify the collapsed bar is visible instead of the expanded one
    assert not window.frame_playbook.isVisible()
    assert window.playbook_collapsed_bar.isVisible()

    # 3. Simulate click on the expand button
    qtbot.mouseClick(expand_button, qt_api.QtCore.Qt.LeftButton)
    # 4. Verify the expanded bar is visible and collapsed is not
    assert window.frame_playbook.isVisible()
    assert not window.playbook_collapsed_bar.isVisible()