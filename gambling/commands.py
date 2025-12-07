from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DrawCardCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.draw_card_action()

class DiscardCardCommand(Command):
    def __init__(self, model, hand_index):
        self.model = model
        self.index = hand_index

    def execute(self):
        self.model.discard_card(self.index)

class MoveToComboCommand(Command):
    def __init__(self, model, hand_index):
        self.model = model
        self.index = hand_index

    def execute(self):
        self.model.move_hand_to_combo(self.index)

class ReturnToHandCommand(Command):
    def __init__(self, model, combo_index):
        self.model = model
        self.index = combo_index

    def execute(self):
        self.model.return_combo_to_hand(self.index)

class ResetGameCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.start_game()
