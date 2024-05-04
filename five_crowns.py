import itertools as it
import copy

from scoring import score_hand
from deck import Deck, Card
from constants import DRAW_CARD, GET_DISCARD

RANKS = range(3, 14)
SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades', 'Stars']
JOKERS = 3


class Game:
    """
    Represents a 5 crown game session
    """

    def __init__(self, ranks=RANKS, suits=SUITS, jokers=JOKERS, players=2, epoch=3):
        """
        Create New Game
        """
        # Deck info
        self._ranks = ranks
        self._suits = suits
        self._jokers = jokers
        self._deck = Deck(ranks, suits, jokers, 2)
        self._full_deck = Deck(RANKS, SUITS, JOKERS, 2)

        # Game info
        self._epoch = epoch
        self._players = players
        self._active_player = 0
        self._player_hands = [[] for _ in range(players)]
        self._discard_pile = []

        # Going out
        self._go_out = False
        self._remaining_players = players
        self._game_over = False

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

    def num_players(self):
        """
        Return number of players
        """
        return self._players

    def get_full_deck(self):
        """
        Return full deck with no cards missing
        """
        return self._full_deck

    def get_epoch(self):
        """
        Gets epoch number
        """
        return self._epoch
    
    def get_active_player(self):
        """
        Return active player
        """
        return self._active_player

    def get_remaining_players(self):
        """
        Return number of players haven't revealed cards
        """
        return self._remaining_players

    def get_discard_pile(self):
        """
        Returns discard pile
        """
        return self._discard_pile

    def is_game_over(self):
        """
        Return boolean indicating game over
        """
        return self._game_over

    def is_going_out(self):
        """
        Return boolean indicating if players are going out
        """
        return self._go_out

    def card_value(self, card):
        """
        Return score value of card for that epoch
        """
        if card.rank == self._epoch:
            return 20
        return card.rank()

    def initialize_game(self, agents):
        """
        Shuffle deck, hand out cards, and flip initial discard
        """
        self._deck.shuffle()
        # Deal cards
        for i in range(self.num_players()):
            agents[i].hand = self._deck.deal(self._epoch)

        # Flip initial discard
        self._discard_pile.append(self._deck.deal(1)[0])

    def play_round(self, player):
        """
        Play a round of 5 crowns

        Not Going Out: Player draw a card or get last discard, then discard a card
        Going Out: Player take turn and reveal card, showing final score
        """
        if self.is_game_over():
            return

        if player.player_id != self._active_player:
            print("Wrong player taking turn")
            return

        if self._deck.size() == 0:
            # No cards left: Game over
            self._game_over = True
            return

        if self._go_out:
            # Draw Phase
            # print("Card in discard pile: ", self._discard_pile[-1])
            if player.draw_phase(self) == GET_DISCARD:
                player.hand.append(self._discard_pile.pop(-1))
            else:
                player.hand.append(self._deck.deal(1)[0])

            # Discard Phase
            discard = player.discard_phase(self)
            player.hand.remove(discard)
            self._discard_pile.append(discard)

            # Go out Phase
            if self._deck.size() == 0:
                self._game_over = True
            self._remaining_players -= 1
            if self._remaining_players == 0:
                self._game_over = True
        else:
            if player.draw_phase(self) == GET_DISCARD:
                player.hand.append(self._discard_pile.pop(-1))
            else:
                player.hand.append(self._deck.deal(1)[0])

            # Discard Phase
            discard = player.discard_phase(self)
            player.hand.remove(discard)
            self._discard_pile.append(discard)

            # Go out Phase
            if self._deck.size() == 0:
                self._game_over = True
            if score_hand(player.hand,self) == 0:
                self._remaining_players -= 1
                self._go_out = True

        self._active_player = (self._active_player + 1) % self.num_players()
