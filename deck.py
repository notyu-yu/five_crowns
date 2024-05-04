import itertools as it
import random


class Card:
    """
    Represents a card of given suit and rank
    """

    def __init__(self, rank, suit):
        '''
        Creates card of a given rank and suit

        rank -- integer
        suit -- character
        '''
        self._rank = rank
        self._suit = suit
        self._hash = str(self).__hash__()

    def rank(self):
        return self._rank

    def suit(self):
        return self._suit

    def __repr__(self):
        # For printing
        return str(self._rank)+str(self._suit)

    def __eq__(self, other):
        # Checking equivalence
        return self._rank == other._rank and self._suit == other._suit

    def __hash__(self):
        # For using a hash key
        return self._hash


class Deck:
    """
    Represents a one-time use deck of cards
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
            self._cards.extend(
                map(lambda c: Card(*c), it.product(ranks, suits)))
            self._cards.extend([Card(50, 'J') for _ in range(jokers)])

    def shuffle(self):
        """
        Shuffles deck
        """
        random.shuffle(self._cards)

    def size(self):
        """
        Return number of remaining cards
        """
        return len(self._cards)

    def deal(self, n):
        """
        Remove and return next n cards

        n -- Interger between 0 and dech size
        """
        dealt = self._cards[-n:]
        dealt.reverse()
        del self._cards[-n:]
        return dealt

    def get_cards(self):
        """
        Get set of cards
        """
        return self._cards
    
    def draw(self):
        """
        Draw one card from deck
        """
        if self.size() > 0:
            card = random.choice(self._cards)
            self._cards.remove(card)
            return card
