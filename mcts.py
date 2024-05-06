import math
import time
import random


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


def simulate(state):
    while not state.is_terminal():
        action = random.choice(state.get_actions())
        new_state = state.successor(action)
        state = new_state
    payoff = state.payoff()
    return payoff


def mcts_policy(cpu_time, player_id):
    
    def search_policy(state):
        root = Node(state)
        node_registry = dict()

        end_time = time.time() + cpu_time
        while time.time() < end_time:
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
            payoff = simulate(node.state)

            # Backpropagation
            while node.parent is not None:
                node.n += 1
                node.r += payoff if node.parent.state.actor() == player_id else -payoff
                node = node.parent

        best_reward = -float("inf")
        best_action = None
        # print(root.state.curr_player_hand)
        for edge in root.edges:
            reward = edge.child.r / edge.child.n
            if reward > best_reward:
                best_reward = reward
                best_action = edge.action

        return best_action

    return search_policy
