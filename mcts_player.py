import copy
from player import Player
from constants import DRAW_CARD, GET_DISCARD
from mcts import mcts_policy
from state import State
from scoring import get_best_discard

class MCTSPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.policy = mcts_policy(1, player_id)
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
        # Randomize deck and player hands
        temp_game = copy.deepcopy(game)
        for player in temp_game._players:
            if player.player_id != game.get_active_player():
                temp_game._deck._cards.extend(player.hand)
        temp_game._deck.shuffle
        for player in temp_game._players:
            if player.player_id != game.get_active_player():
                player.hand = temp_game._deck.deal(temp_game.get_epoch())
        state = State(temp_game, is_root=True, root_card=self.prev_discard)
        return self.policy(state)[1]
