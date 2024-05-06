import math
import time
import random
from copy import deepcopy
from random_player import RandomPlayer
from scoring import score_hand

DEPTH = 20

class Edge:
    def __init__(self, child, action=None):
        self.child = child
        self.action = action
        self.n = 0


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.edges = []
        self.n = 0
        self.r = 0
        self.unused_actions = state.get_actions()
        self.parent = parent

    def best_child(self):
        T = sum(e.n for e in self.edges)
        max_ucb = -float("inf")
        max_index = -1
        for i, e in enumerate(self.edges):
            exploitation = e.child.r / e.child.n if e.child.n > 0 else 0
            exploration = math.sqrt(2 * math.log(T) / e.n) if e.n > 0 else 0
            ucb = exploitation + exploration
            if ucb > max_ucb:
                max_ucb = ucb
                max_index = i
        return max_index

    def is_expanded(self):
        return len(self.edges) == len(self.state.get_actions())


def partial_score(hand,game):
    score = score_hand(hand,game)
    return (100 if score == 0 else 0) - score


def simulate(state):
    d = 0
    temp_game = deepcopy(state.game)
    temp_players = [RandomPlayer(i) for i in range(temp_game.num_players())]
    temp_hands = [deepcopy(player.hand) for player in temp_game._players]
    for player,new_hand in zip(temp_players,temp_hands):
        player.hand = new_hand
    temp_game._players = temp_players
    while not temp_game.is_game_over() and d < DEPTH:
        temp_game.play_round()
        d += 1
    return [partial_score(temp_game._players[i].hand,temp_game) for i in range(temp_game.num_players())]


def mcts_policy(cpu_time, player_id):
    
    def search_policy(state):
        root = Node(state)
        node_registry = dict()

        end_time = time.time() + cpu_time
        iters = 0
        while time.time() < end_time:
            iters += 1
            node = root
            
            # Traversal
            while node.is_expanded() and not node.state.is_terminal():
                index = node.best_child()
                best_child = node.edges[index].child
                best_child.parent = node
                node.edges[index].n += 1
                node = best_child

            # Expansion
            if not node.state.is_terminal():
                action = node.unused_actions.pop()
                new_state = node.state.successor(action)
                if new_state in node_registry:
                    child = node_registry[new_state]
                else:
                    child = Node(new_state, node)
                    node_registry[new_state] = child
                edge = Edge(child, action)
                edge.n += 1
                node.edges.append(edge)
                node = child

            # Simulation
            payoff_array = simulate(node.state)

            # Backpropagation
            seen_nodes = set([node])
            while node.parent is not None:
                node.n += 1
                node.r += payoff_array[node.parent.state.actor()]
                node = node.parent
                assert node not in seen_nodes, "loop detected"
                seen_nodes.add(node)

        best_reward = -float("inf")
        best_action = None
        # print(root.state.curr_player_hand)
        for edge in root.edges:
            reward = edge.child.r / edge.child.n
            if reward > best_reward:
                best_reward = reward
                best_action = edge.action
        
        if not best_action:
            print('iters',iters)
            print(root.edges)
        return best_action

    return search_policy
