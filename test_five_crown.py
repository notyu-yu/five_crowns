from five_crowns import Game
from greedy import GreedyPlayer
from scoring import score_hand

def simulate_one_game():
    game = Game(players=4)
    players = [GreedyPlayer(i) for i in range(4)]
    game.initialize_game(players)

    while not game.is_game_over():
        game.play_round(players[game.get_active_player()])
    
    for player in players:
        print(score_hand(player.hand,game,keep_wild=False))

simulate_one_game()