from player import Player
from scoring import get_best_discard
from constants import GET_DISCARD, DRAW_CARD
import copy
import torch
from dqn_infer import inference

class DQNPlayer(Player):
    """
    DQN player always takes action that minimize score for turn
    """
    def __init__(self, player_id):
        super().__init__(player_id)
        self.prev_discard = None

    def draw_phase(self, game):
        # Get best score if we take discard
        new_card = game.get_discard_pile()[-1]
        temp_hand = self.hand + [new_card]
        _, discard_score = get_best_discard(temp_hand,game,excluded_discard=new_card)

        # Get best expected score if we draw random
        remaining_deck = copy.deepcopy(game.get_full_deck().get_cards())
        draw_scores = []
        for card in game.get_discard_pile() + self.hand:
            remaining_deck.remove(card)
        for card in remaining_deck:
            temp_hand = self.hand + [card]
            _, draw_score = get_best_discard(temp_hand, game)
            draw_scores.append(draw_score)
        expected_draw_score = sum(draw_scores)/len(draw_scores)

        # Take action with better expected score
        if discard_score < expected_draw_score:
            self.prev_discard = game.get_discard_pile()[-1]
            return GET_DISCARD
        self.prev_discard = None
        return DRAW_CARD

    def discard_phase(self, game):
        action = inference(game, self.hand, self.prev_discard)
        return action
