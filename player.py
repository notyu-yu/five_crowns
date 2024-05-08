"""
Player class and HumanPlayer class
"""

from abc import ABC, abstractmethod


class Player(ABC):
    """
    Player class
    
    Attributes:
        player_id (int): Player ID
        hand (list): List of cards in hand
        
    Methods:
        show_hand: Show hand of player
        draw_phase: Draw phase for player
        discard_phase: Discard phase for player
    """
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
