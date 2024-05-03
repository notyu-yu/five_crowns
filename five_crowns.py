import itertools as it
import copy

import scoring
from deck import Deck, Card


class Game:
    """
    Represents a 5 crown game session
    """

    def __init__(self, ranks, suits, jokers):
        """
        Create New Game
        """
        self._ranks = ranks
        self._suits = suits
        self._jokers = jokers
        self._epoch = 3

    def all_ranks(self):
        """
        Return all ranks
        """
        return self._ranks

    def all_suits(self):
        """
        Return all suits
        """
        return self._suits

    def num_jokers(self):
        """
        Return number of jokers
        """
        return self._jokers

    def card_value(self, card):
        """
        Return score value of card for that epoch
        """
        if card.rank == self._epoch:
            return 20
        else:
            return card.rank()

