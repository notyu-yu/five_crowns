import argparse
from multiprocessing import Pool

from five_crowns import Game
from greedy import GreedyPlayer
from random_player import RandomPlayer
from scoring import score_hand

PLAYERS = 4
EPOCH = 5
THREADS = 10

def parse_args():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser()

    '''
    task = parser.add_mutually_exclusive_group()
    task.add_argument('--find', action="store_true")
    task.add_argument('--verify', action="store_true")

    parser.add_argument('--tolerance', type=float, default=1e-6)

    scoring = parser.add_mutually_exclusive_group()
    scoring.add_argument('--win', action="store_true")
    scoring.add_argument('--score', action="store_true")
    scoring.add_argument('--lottery', action="store_true")

    parser.add_argument('--units', type=int)

    parser.add_argument('values', nargs='+', type=int)
    '''

    parser.add_argument('--iters', type=int)

    args_out = parser.parse_args()

    return args_out

def simulate_one_game(agents,epoch=EPOCH):
    '''
    Simulate one game with given parameters
    Return player 1 score
    '''
    game = Game(players=len(agents),epoch=epoch)
    players = [(agents[i])(i) for i in range(len(agents))]
    game.initialize_game(players)

    while not game.is_game_over():
        game.play_round(players[game.get_active_player()])

    score = score_hand(players[0].hand,game)
    
    return score


if __name__ == '__main__':
    args = parse_args()

    agent_policies = [GreedyPlayer] + [RandomPlayer for i in range(1,PLAYERS)]
    for epoch_number in range(3,6):
        with Pool(processes = THREADS) as pool:
            scores = pool.map(simulate_one_game,[agent_policies]*args.iters)
        print(f'Game for Epoch {epoch_number}')
        print(f'Win Rate: {sum([1 for i in scores if i == 0])/args.iters}')
        print(f'Average Score: {sum(scores)/args.iters}')
