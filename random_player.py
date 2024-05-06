import itertools as it
import random

from player import Player
from constants import GET_DISCARD, DRAW_CARD


class RandomPlayer(Player):
    """
    Randomly choose actions
    """

    def draw_phase(self, game):
        return random.choice([GET_DISCARD, DRAW_CARD])

    def discard_phase(self, game):
        return random.choice(self.hand)
