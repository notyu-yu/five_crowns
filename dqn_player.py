import copy
import torch

from dqn import DQN
from player import Player
from dqn_infer import inference
from scoring import get_best_discard
from constants import GET_DISCARD, DRAW_CARD


class DQNPlayer(Player):
    """
    DQN Player

    Args:
        player_id (int): Player ID

    Attributes:
        player_id (int): Player ID
        prev_discard (Card): Previous discard card
        epsilon (float): Exploration rate
        prev_action (int): Previous action
        policy_net (DQN): Policy network

    Methods:
        draw_phase: Draw phase for DQN Player
        discard_phase: Discard phase for DQN Player
    """

    def __init__(self, player_id):
        self.player_id = player_id
        self.prev_discard = None
        self.epsilon = 0.05
        self.prev_action = None
        self.policy_net = DQN(113, 56).to("cuda")
        self.policy_net.load_state_dict(torch.load(f"five_crowns_dqn_{3}.pth"))
        self.policy_net.eval()

    def draw_phase(self, game):
        """
        Draw phase for DQN Player

        Args:
            game (Game): Game object

        Returns:
            int: Action to take
        """
        # Get best expected score if we discard the last card
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
            self.prev_discard = game.get_discard_pile()[-1]
            return GET_DISCARD
        self.prev_discard = None
        return DRAW_CARD

    def discard_phase(self, game):
        """
        Discard phase for DQN Player

        Args:
            game (Game): Game object

        Returns:
            Card: Card to discard
        """
        # Perform inference
        with torch.no_grad():
            action = inference(game, self.hand, self.prev_discard, self.policy_net)

        return action
