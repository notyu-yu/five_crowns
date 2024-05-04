from abc import ABC, abstractmethod

from constants import DRAW_CARD, GET_DISCARD

class Player(ABC):
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []

    def show_hand(self):
        print(f"Player {self.player_id}'s hand: {self.hand}")

    @abstractmethod
    def draw_phase(self, game):
        pass

    @abstractmethod
    def discard_phase(self, game):
        pass

class HumanPlayer(Player):
    def draw_phase(self, game):
        while True:
            self.show_hand()
            choice = input("Would you like to draw from the deck or the discard pile? (deck/discard): ").lower()
            if choice != "deck" or choice != "discard":
                print("Please enter a valid action.")
            else:
                return DRAW_CARD if choice == "deck" else GET_DISCARD
            
    def discard_phase(self, game):
        while True:
            self.show_hand()
            discard = input("Which card would you like to discard?: ")
            if discard in self.hand:
                print("Please choose a card in your hand.")
            else:
                return discard
