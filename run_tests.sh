cat README.md

echo "=============================="
echo "Sample run of 50 games"
# Random
echo "Testing random vs random"
python test_five_crown.py --iters ${1:-50} --agent random --opponent random
echo "=========="
echo "Testing random vs greedy"
python test_five_crown.py --iters ${1:-50} --agent random --opponent greedy
echo "=========="
# Greedy
echo "Testing greedy vs random"
python test_five_crown.py --iters ${1:-50} --agent greedy --opponent random
echo "=========="
echo "Testing greedy vs greedy"
python test_five_crown.py --iters ${1:-50} --agent greedy --opponent greedy
echo "=========="
# MCTS
echo "Testing mcts vs random"
python test_five_crown.py --iters ${1:-50} --agent mcts --opponent random
echo "=========="
echo "Testing mcts vs greedy"
python test_five_crown.py --iters ${1:-50} --agent mcts --opponent greedy
echo "=========="
# DQN
echo "Testing dqn vs random"
python test_five_crown.py --iters ${1:-50} --agent dqn --opponent random
echo "=========="
echo "Testing dqn vs greedy"
python test_five_crown.py --iters ${1:-50} --agent dqn --opponent greedy
echo "=========="
