import random

class AppController():
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._setup_signals()

    def _setup_signals(self):
        #Connect push to talk button and dropdown list to handlers
        self.view.button_push_to_talk.clicked.connect(self.radio_sim)
        self.view.procedure_dropdown.currentTextChanged.connect(self.handle_dropdown_change)

    def radio_sim(self):
        self.view.text_playbook.setText(random.choice(self.model.playbook))

    def handle_dropdown_change(self, new_value):
        self.model.selected_procedure = new_value
        #print(f"Selected procedure: {self.model.selected_procedure}")