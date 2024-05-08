import argparse

from multiprocessing import Pool

from five_crowns import Game
from scoring import score_hand
from greedy import GreedyPlayer
from mcts_player import MCTSPlayer
from random_player import RandomPlayer
from dqn_player import DQNPlayer

PLAYERS = 4
EPOCH = 4
THREADS = 14

AGENT_MAP = {
    'greedy':GreedyPlayer,
    'mcts':MCTSPlayer,
    'random':RandomPlayer,
    'dqn':DQNPlayer
}

def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--iters", type=int, default=100)
    parser.add_argument("--agent", type=str, default="greedy")
    parser.add_argument("--opponent", type=str, default="random")

    args_out = parser.parse_args()

    return args_out


def simulate_one_game(args):
    """
    Simulate one game with given parameters
    Return player 1 score
    """
    agents, epoch = args
    players = [(agents[i])(i) for i in range(len(agents))]
    game = Game(players=players, epoch=epoch)
    game.initialize_game()

    while not game.is_game_over():
        game.play_round()

    score = score_hand(players[0].hand, game)

    return score


if __name__ == "__main__":
    args = parse_args()

    agent_policies = [AGENT_MAP[args.agent]] + [AGENT_MAP[args.opponent] for i in range(1, PLAYERS)]
    for epoch_number in range(3, 4):
        with Pool(processes=THREADS) as pool:
            scores = pool.map(simulate_one_game, [(agent_policies,epoch_number)] * args.iters)
        print(f"Game for Epoch {epoch_number}")
        print(f"Win Rate: {sum([1 for i in scores if i == 0])/args.iters}")
        print(f"Average Score: {sum(scores)/args.iters}")
