"""
State class for MCTS
"""

from copy import deepcopy

from scoring import score_hand


class State:
    """
    A State class to represent the state of a game
    """

    def __init__(self, game, is_root=False, root_card = None):
        self.is_root = is_root
        self.root_card = root_card
        self.game = deepcopy(game)
        self.num_players = self.game.num_players()
        self.curr_player_id = self.game.get_active_player()
        self.curr_player_hand = self.game.get_player_hand(self.curr_player_id)
        self.discard_pile_card = (
            self.game.get_discard_pile(
            )[-1] if self.game.get_discard_pile() else False
        )

    def is_terminal(self):
        """
        Determines whether the current state is a terminal state or not

        Returns:
            - bool: True if the game is over else False
        """
        return self.game.is_game_over() or ((not self.is_root) and (self.game.get_deck().size() == 0 or score_hand(self.curr_player_hand, self.game) == 0))

    def get_actions(self):
        """
        Returns all possible actions from the current state
        """
        if self.is_root:
            actions = [("root", c) for c in self.curr_player_hand if c != self.root_card]

        else:
            # initialize actions list
            actions = []

            if self.discard_pile_card:
                #actions.append(("discard", self.discard_pile_card))
                for card in self.curr_player_hand:
                    actions.append(("discard", card))
            if self.game.get_deck():
                actions.append(("deck", None))
                for card in self.curr_player_hand:
                    actions.append(("deck", card))

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

        # Get the actions
        first_action = action[0]
        second_action = action[1]

        # Execute the first action
        added_card = None
        if first_action == "deck":
            added_card = new_state.get_deck().draw()
            new_state.get_player_hand(self.curr_player_id).append(added_card)
        elif first_action == "discard":
            added_card = new_state.get_discard_pile().pop()
            new_state.get_player_hand(self.curr_player_id).append(added_card)

        # Execute the second action
        if second_action == None:
            new_state.get_player_hand(self.curr_player_id).remove(added_card)
            new_state.get_discard_pile().append(added_card)
        else:
            new_state.get_player_hand(
                self.curr_player_id).remove(second_action)
            new_state.get_discard_pile().append(second_action)

        # Check the hand score and update game ending conditions
        # print(new_state.get_player_hand(self.curr_player_id))
        hand_score = score_hand(
            new_state.get_player_hand(self.curr_player_id), new_state
        )
        if hand_score == 0:
            new_state._go_out = True
            if new_state._remaining_players == new_state.num_players():
                new_state._go_out_player = self.curr_player_id
            new_state._remaining_players -= 1
            if new_state._remaining_players == 0:
                new_state._game_over = True

        return State(new_state)

    def payoff(self):
        """
        Calculates the reward for the player at this state

        Returns:
            int: The reward for the current player in the state
        """
        if not self.game._go_out:
            return 0
        # print(self.game.get_player_hand(self.curr_player_id))
        hand_score = score_hand(
            self.game.get_player_hand(self.curr_player_id), self.game
        )
        return 1 if hand_score == 0 else -1

    def actor(self):
        """
        Determines the ID of the current player

        Returns:
            - int: The ID of the current player
        """
        return self.curr_player_id

    def __hash__(self):
        return hash(
            (self.game)
        )

    def __eq__(self, other):
        return (
            self.curr_player_id == other.curr_player_id
            and self.curr_player_hand == other.curr_player_hand
            and self.discard_pile_card == other.discard_pile_card
        )
