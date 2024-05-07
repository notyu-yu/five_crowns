# Greedy
pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent greedy > greedy_greedy.txt
pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent random > greedy_random.txt
pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent mcts > greedy_mcts.txt
# MCTS
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent greedy > mcts_greedy.txt
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent random > mcts_random.txt
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent mcts > mcts_mcts.txt
# Random
pypy3 test_five_crown.py --iters 10000 --agent random --opponent greedy > random_greedy.txt
pypy3 test_five_crown.py --iters 10000 --agent random --opponent random > random_random.txt
pypy3 test_five_crown.py --iters 10000 --agent random --opponent mcts > random_mcts.txt
