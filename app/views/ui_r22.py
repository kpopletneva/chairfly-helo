from PySide6 import QtCore, QtWidgets, QtGui
from views.styles import StyleSheet

class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._setup_window()
        self._setup_widgets()

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
        self.layout_main = QtWidgets.QHBoxLayout(central_widget)

        # Left side:vertical frame (takes 50% width, 100% height)
        # Frame for cockpit mockup and push-to-talk button
        frame_cockpit, layout_cockpit = self.create_framed_widget("Cockpit mockup goes here (50%)", "#e6f7ff")
        layout_cockpit.addStretch()
        self.layout_main.addWidget(frame_cockpit, 2)
        
        # Right side: contains two vertical frames
        # Frame for checklist and procedure drop-down
        self.frame_checklist, layout_checklist = self.create_framed_widget("Checklist goes here (25%)", "#fff0f0")
        # Create checklist dropdown (procedure selector)
        self.procedure_dropdown = self.add_dropdown([
            "Startup",
            "Shutdown",
            "Emergency Procedures"
        ])
        self.checklist_panel, self.checklist_collapse_button, self.checklist_collapsed_bar = self.create_collapsible_panel(
            ">>", "<<", self.frame_checklist, left_widget=self.procedure_dropdown
        )
        layout_checklist.addWidget(self.checklist_panel, alignment=QtCore.Qt.AlignTop)
        self.layout_main.addWidget(self.frame_checklist, 1)

        # Frame for ATC clearances playbook, stretch goal toggles and other configs
        self.frame_playbook, layout_playbook = self.create_framed_widget("Radio playbook goes here (25%)", "#f0fff0")
        self.playbook_panel, self.playbook_collapse_button, self.playbook_collapsed_bar = self.create_collapsible_panel(
            ">>", "<<", self.frame_playbook
        )
        layout_playbook.addWidget(self.playbook_panel, alignment=QtCore.Qt.AlignTop)
        self.layout_main.addWidget(self.frame_playbook, 1)

        self.button_push_to_talk = QtWidgets.QPushButton("PUSH TO TALK", parent=central_widget)
        self.button_push_to_talk.setStyleSheet(StyleSheet.red_rounded_button())
        self.button_push_to_talk.setMouseTracking(True)
        layout_cockpit.addWidget(self.button_push_to_talk, alignment=QtCore.Qt.AlignBottom)

        # Text widget for ATC clearances playbook
        self.text_playbook = QtWidgets.QLabel("",
                                     alignment=QtCore.Qt.AlignCenter, parent=central_widget)
        self.text_playbook.setWordWrap(True)  #Enable breaking lines inside the current layout width
        self.text_playbook.setMouseTracking(True)
        layout_playbook.addWidget(self.text_playbook)

    def add_dropdown(self, items):
        """Create dropdown widget with given items."""
        dropdown = QtWidgets.QComboBox()
        dropdown.addItems(items)
        dropdown.setStyleSheet(StyleSheet.dropdown_style())
        selected_item = dropdown.currentText()
        selected_index = dropdown.currentIndex()

        return dropdown

    def create_collapsible_panel(self, text_collapse, text_expand, frame_to_toggle, left_widget=None):
        """
        - Adds a toggle button (and optional left-aligned widget) inside a horizontal layout to the top of a frame_to_toggle.
        - Adds a thin vertical collapsed panel with a toggle button to the right when collapsed.

        :param text_collapse: Text shown when frame is expanded (e.g. '>>')
        :param text_expand: Text shown when frame is collapsed (e.g. '<<')
        :param frame_to_toggle: A QFrame to show/hide
        :param left_widget: Optional widget (e.g. dropdown) shown on the left of the toggle
        :return: QHBoxLayout containing the toggle row
        """
        # Main container panel
        panel = QtWidgets.QWidget()
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar with toggle + optional left widget
        collapse_button = QtWidgets.QToolButton(text=text_collapse)
        collapse_button.setStyleSheet(StyleSheet.toggle_style())
        collapse_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Create horizontal layout
        top_row = QtWidgets.QWidget()
        top_row_layout = QtWidgets.QHBoxLayout(top_row)
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        if left_widget:
            top_row_layout.addWidget(left_widget)
            top_row_layout.addStretch()
        top_row_layout.addWidget(collapse_button, alignment=QtCore.Qt.AlignRight)

        # Hidden version shown when collapsed
        collapsed_bar = QtWidgets.QToolButton(text=text_expand)
        collapsed_bar.setStyleSheet(StyleSheet.toggle_style())
        collapsed_bar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        collapsed_bar.setVisible(False)

        #Thin vertical collapsed panel
        panel_layout.addWidget(collapsed_bar, alignment=QtCore.Qt.AlignTop)
        self.layout_main.addWidget(panel)

        # Toggle behavior
        def collapse():
            frame_to_toggle.setVisible(False)
            if left_widget:
                left_widget.setVisible(False)
            collapse_button.setVisible(False)
            collapsed_bar.setVisible(True)

        def expand():
            frame_to_toggle.setVisible(True)
            if left_widget:
                left_widget.setVisible(True)
            collapse_button.setVisible(True)
            collapsed_bar.setVisible(False)

        collapse_button.clicked.connect(collapse)
        collapsed_bar.clicked.connect(expand)

        return top_row, collapse_button, collapsed_bar

    def create_framed_widget(self, text, color):
        """
        Creates a scrollable QFrame with automatic scrollbars if content exceeds the visible area.

        :param text (str): (Currently unused) Placeholder for optional label text
        :param color (str): Background color of the frame (hex or named value)
        :return tuple:
            - QScrollArea: The scrollable container holding the frame
            - QVBoxLayout: The layout inside the frame to which widgets can be added
        """
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)  # Box, Panel, StyledPanel, etc.
        frame.setFrameShadow(QtWidgets.QFrame.Plain)  # Raised, Sunken, Plain
        frame.setLineWidth(1)
        frame.setStyleSheet(StyleSheet.frame_style(color))
        #Prevent the frame from stretching vertically or horizontally
        frame.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        frame_layout = QtWidgets.QVBoxLayout(frame)
        #frame_label = QtWidgets.QLabel(text)
        #frame_label.setAlignment(QtCore.Qt.AlignCenter)
        #Add a scroll bar to a frame appearing if contents exceed available space
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(frame)
        scroll.setMouseTracking(True)
        frame.setMouseTracking(True)

        return scroll, frame_layout

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
        """Resizes to match screen resolution."""
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.resize(screen_geometry.width(), screen_geometry.height())
        self.move(screen_geometry.topLeft())
