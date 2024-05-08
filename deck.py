"""
Creates Card and Deck classes for card games
"""

import random
import itertools as it


class Card:
    """
    Represents a card of given rank and suit

    Methods:
        rank(): Return rank of card
        suit(): Return suit of card
    """

    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit
        self._hash = str(self).__hash__()

    def rank(self):
        """
        Return rank of card

        Returns:
            int: Rank of card
        """
        return self._rank

    def suit(self):
        """
        Return suit of card

        Returns:
            str: Suit of card
        """
        return self._suit

    def __repr__(self):
        # For printing
        return str(self._rank) + str(self._suit)

    def __eq__(self, other):
        # Checking equivalence
        if isinstance(other, Card):
            return self._rank == other._rank and self._suit == other._suit
        return False

    def __hash__(self):
        # For using a hash key
        return self._hash


class Deck:
    """
    Represents a one-time use deck of cards

    Methods:
        shuffle(): Shuffle deck
        size(): Return number of remaining cards
        deal(n): Remove and return next n cards
        get_cards(): Get set of cards
        draw(): Draw one card from deck
    """

    def __init__(self, ranks, suits, jokers, copies):
        """
        Create a deck of cards for the given ranks and suits, with
        given number of jokers, and makes a certain number of copies
        of such decks to shuffle together

        Jokers have suit J and rank 50

        ranks -- iterable of positive integers
        suits -- iterable
        jokers -- nonnegatie integer
        copies -- nonnegative integer
        """
        self._cards = []
        for _ in range(copies):
            self._cards.extend(map(lambda c: Card(*c), it.product(ranks, suits)))
            self._cards.extend([Card(50, "J") for _ in range(jokers)])

    def shuffle(self):
        """
        Shuffles deck
        """
        random.shuffle(self._cards)

    def size(self):
        """
        Return number of remaining cards

        Returns:
            int: Number of cards left in deck
        """
        return len(self._cards)

    def deal(self, n):
        """
        Remove and return next n cards

        Returns:
            list: List of n cards
        """
        dealt = self._cards[-n:]
        dealt.reverse()
        del self._cards[-n:]
        return dealt

    def get_cards(self):
        """
        Get set of cards

        Returns:
            list: List of cards
        """
        return self._cards

    def draw(self):
        """
        Draw one card from deck

        Returns:
            Card: Card drawn
        """
        if self.size() > 0:
            card = random.choice(self._cards)
            self._cards.remove(card)
            return card
