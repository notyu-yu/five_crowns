"""
Greedy player always takes action that minimize score for turn
"""

import copy

from player import Player
from scoring import get_best_discard
from constants import GET_DISCARD, DRAW_CARD


class GreedyPlayer(Player):
    """
    Greedy player class

    Attributes:
        player_id (int): Player ID
        hand (list): List of cards in hand

    Methods:
        draw_phase: Draw phase for Greedy Player
        discard_phase: Discard phase for Greedy Player
    """

    def draw_phase(self, game):
        """
        Greedy player always takes action that minimize score for turn

        Args:
            game (Game): Game object

        Returns:
            int: Action to take
        """
        # Get best score if we take discard
        new_card = game.get_discard_pile()[-1]
        temp_hand = self.hand + [new_card]
        _, discard_score = get_best_discard(temp_hand, game, excluded_discard=new_card)

        # Get best expected score if we draw random
        remaining_deck = copy.deepcopy(game.get_full_deck().get_cards())
        draw_scores = []
        for card in game.get_discard_pile() + self.hand:
            remaining_deck.remove(card)
        for card in remaining_deck:
            temp_hand = self.hand + [card]
            _, draw_score = get_best_discard(temp_hand, game)
            draw_scores.append(draw_score)
        expected_draw_score = sum(draw_scores) / len(draw_scores)

        # Take action with better expected score
        if discard_score < expected_draw_score:
            return GET_DISCARD
        return DRAW_CARD

    def discard_phase(self, game):
        """
        Greedy player always takes action that minimize score for turn

        Args:
            game (Game): Game object

        Returns:
            Card: Card to discard
        """
        discard, _ = get_best_discard(self.hand, game)
        return discard
