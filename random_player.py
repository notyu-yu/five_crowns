"""
Random Player class
"""

import random

from player import Player
from constants import GET_DISCARD, DRAW_CARD


class RandomPlayer(Player):
    """
    Randomly choose actions

    Attributes:
        player_id (int): Player ID
        hand (list): List of cards in hand

    Methods:
        draw_phase: Draw phase for Random Player
        discard_phase: Discard phase for Random Player
    """

    def draw_phase(self):
        """
        Randomly choose between drawing from deck or discard pile

        Returns:
            int: Action to take
        """
        return random.choice([GET_DISCARD, DRAW_CARD])

    def discard_phase(self):
        """
        Randomly choose a card to discard

        Returns:
            Card: Card to discard
        """
        return random.choice(self.hand)
