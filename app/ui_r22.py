import random
from PySide6 import QtCore, QtWidgets, QtGui

class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._setup_window()
        self._setup_widgets()
        self._setup_signals()

    def _setup_window(self):
        self.setWindowTitle("ChairFly Trainer")

        # Install an event filter to catch mouse movements over the window
        self.setMouseTracking(True)
        self.installEventFilter(self)

        # Track whether fullsceen mode in on/ off
        self._is_fullscreen = True

        # Track whether title bar is currently shown (False = hidden)
        self._title_shown = False

        # Timer to hide the title bar a short moment after the mouse moves out of 5 top pixels
        self._hide_timer = QtCore.QTimer(self)
        self._hide_timer.setInterval(800)
        self._hide_timer.timeout.connect(self._hide_title_bar)

    def _setup_widgets(self):
        # Create central child widget under main window to host everything else
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        # Ensure central child widget also tracks mouse
        central_widget.setMouseTracking(True)
        # Main horizontal layout
        layout_main = QtWidgets.QHBoxLayout(central_widget)

        # Left side:vertical frame (takes 50% width, 100% height)
        # Frame for cockpit mockup and push-to-talk button
        frame_cockpit, layout_cockpit = self.create_framed_widget("Cockpit mockup goes here (50%)", "#e6f7ff")
        layout_cockpit.addStretch()
        layout_main.addWidget(frame_cockpit, 2)
        
        # Right side: contains two vertical frames
        # Frame for checklist and procedure drop-down
        frame_checklist, layout_checklist = self.create_framed_widget("Checklist goes here (25%)", "#fff0f0")
        layout_main.addWidget(frame_checklist, 1)

        # Frame for ATC clearances playbook, stretch goal toggles and other configs
        frame_playbook, layout_playbook = self.create_framed_widget("Radio playbook goes here (25%)", "#f0fff0")
        layout_main.addWidget(frame_playbook, 1)

        # "push-to-talk" button
        self.button_style = """
        QPushButton {
            background-color: red;
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #cc0000; /* slightly darker red */
        }
        QPushButton:pressed {
            background-color: #990000; /* even darker red for pressed state */
        }
        """
        self.button_push_to_talk = QtWidgets.QPushButton("PUSH TO TALK", parent=central_widget)
        self.button_push_to_talk.setStyleSheet(self.button_style)
        self.button_push_to_talk.setMouseTracking(True)
        layout_cockpit.addWidget(self.button_push_to_talk, alignment=QtCore.Qt.AlignBottom)

        # Text widget for ATC clearances playbook
        self.text = QtWidgets.QLabel("",
                                     alignment=QtCore.Qt.AlignCenter, parent=central_widget)
        self.text.setMouseTracking(True)
        layout_playbook.addWidget(self.text)

    def _setup_signals(self):
        #Connect push to talk button to slot
        self.playbook = ["Helicopter 603HH. Runway 25 cleared for takeoff. Lacamas Lake departure approved", "Helicopter 603HH. Runway 25 cleared to land. Make right traffic.", "Helicopter 603HH. Make right 180 for spacing.", "Привет мир"]
        self.button_push_to_talk.clicked.connect(self.radio_sim)

    def create_framed_widget(self, text, color):
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.Box)  # Box, Panel, StyledPanel, etc.
        frame.setFrameShadow(QtWidgets.QFrame.Raised)  # Raised, Sunken, Plain
        frame.setLineWidth(2)
        frame.setStyleSheet(f"background-color: {color};")
        frame_layout = QtWidgets.QVBoxLayout(frame)
        #frame_label = QtWidgets.QLabel(text)
        #frame_label.setAlignment(QtCore.Qt.AlignCenter)
        frame.setMouseTracking(True)

        return frame, frame_layout

    @QtCore.Slot()
    def radio_sim(self):
        self.text.setText(random.choice(self.playbook))

    def keyPressEvent(self, event):
        """Catch Esc key to leave full‐screen."""
        if event.key() == QtCore.Qt.Key_Escape and self._is_fullscreen:
            # Restore normal window with title bar, exit fullscreen mode:
            self.exit_fullscreen()
        elif event.key() == QtCore.Qt.Key_F11 and not self._is_fullscreen:
            # Enter fullscreen mode:
            self.enter_fullscreen()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, watched, event):
        """
        Watch for MouseMove events. When the cursor is near the top edge (y <= threshold),
        show the title bar and restart the hide timer.
        """
        if watched is self and event.type() == QtCore.QEvent.MouseMove:
            pos = event.position().toPoint()
            # If cursor is within the top 5 pixels of the window
            if pos.y() <= 5 and self._is_fullscreen:
                # If title is not already shown, show it
                if not self._title_shown:
                    self._show_title_bar()
                # If a hide timer was running, cancel it:
                if self._hide_timer.isActive():
                    self._hide_timer.stop()
            # If cursor is lower than the top 5 pixels of the window
            elif pos.y() > 5 and self._is_fullscreen:
                # Only start or keep the hide timer if title is currently shown
                if self._title_shown and not self._hide_timer.isActive():
                    self._hide_timer.start()
        return super().eventFilter(watched, event)

    def _hide_title_bar(self):
        """Add FramelessWindowHint and show full screen."""
        flags = self.windowFlags()
        self.setWindowFlags(flags | QtCore.Qt.FramelessWindowHint)
        # Re-show the window after changing flags (adding FramelessWindowHint)
        self.showFullScreen()
        self._title_shown = False

    def _show_title_bar(self):
        """Add back the title bar, then reapply full screen."""
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~QtCore.Qt.FramelessWindowHint)
        # Re-show the window maximized after changing flags (removing FramelessWindowHint)
        self.showMaximized()
        self._title_shown = True

    def enter_fullscreen(self):
        """Enters full screen mode."""
        self._hide_title_bar()
        #self.show_fading_message("Press Esc to exit fullscreen mode.") #To develop self.show_fading_message() later
        self._is_fullscreen = True

    def exit_fullscreen(self):
        """Exits full screen mode."""
        self._show_title_bar()
        #self.show_fading_message("Press F11 to re-enter fullscreen mode.") #To develop self.show_fading_message() later
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._is_fullscreen = False

    def resize_fullscreen_dimensions(self):
        """Resizes to match screen resolution"""
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.resize(screen_geometry.width(), screen_geometry.height())
        self.move(screen_geometry.topLeft())