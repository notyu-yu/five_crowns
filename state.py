"""
State class for MCTS
"""
from copy import deepcopy

from scoring import score_hand

class State:
    """
    A State class to represent the state of a game
    """
    def __init__(self, game):
        self.game = deepcopy(game)
        self.num_players = self.game._players
        self.curr_player_id = self.game._active_player
        self.curr_player_hand = self.game._player_hands[self.curr_player_id]
        self.discard_pile_card = self.game._discard_pile[-1]

    def is_terminal(self):
        """
        Determines whether the current state is a terminal state or not

        Returns:
            - bool: True if the game is over else False
        """
        return self.game.game_over()

    def get_actions(self):
        """
        Returns all possible actions from the current state
        """
        # initialize actions list
        actions = [("discard", self.discard_pile_card), ("deck", None)]

        # Add all possible combinations of actions
        for card in self.curr_player_hand:
            actions.extend([("discard", card), ("deck", card)])

        return actions

    def successor(self, action):
        """
        Returns the successor state given the action from the current state

        Args:
            - action: The action to take from the current state
        
        Returns:
            - State: The new state after taking the action
        """
        # Make a copy for the successor state
        new_state = deepcopy(self.game)

        # Get the next player
        next_player_id = (self.curr_player_id + 1) % self.num_players
        new_state._active_player = next_player_id

        # Decompose the action
        first_action, second_action = action

        # Execute the first action
        added_card = None
        if first_action == "deck":
            added_card = new_state._deck.draw()
        elif first_action == "discard":
            added_card = new_state._discard_pile.pop()
        new_state._player_hands[self.curr_player_id].append(added_card)

        # Execute the second action
        new_state._player_hands[self.curr_player_id].remove(second_action)
        new_state._discard_pile.append(second_action)
        
        # Check the hand score and update game ending conditions
        hand_score = score_hand(new_state._player_hands[self.curr_player_id])
        if hand_score == 0:
            new_state._go_out = True
            if new_state._remaining_players == new_state._players:
                new_state._go_out_player = self.curr_player_id
            new_state._remaining_players -= 1
            if new_state._remaining_players == 0:
                new_state._game_over = True

        return new_state

    def payoff(self):
        """
        Calculates the reward for the player at this state

        Returns:
            int: The reward for the current player in the state
        """
        if not self.game._go_out:
            return 0
        hand_score = score_hand(self.game._player_hands[self.curr_player_id])
        return 1 if hand_score == 0 else -1

    def actor(self):
        """
        Determines the ID of the current player

        Returns:
            - int: The ID of the current player
        """
        return self.curr_player_id
