#pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent greedy > greedy_greedy.txt
#pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent random > greedy_random.txt
pypy3 test_five_crown.py --iters 10000 --agent greedy --opponent mcts > greedy_mcts.txt
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent greedy > mcts_greedy.txt
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent random > mcts_random.txt
pypy3 test_five_crown.py --iters 10000 --agent mcts --opponent mcts > mcts_mcts.txt
