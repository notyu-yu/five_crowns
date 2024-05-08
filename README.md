# Five Crowns Agent - A Monte Carlo Tree Search and Deep-Q-Learning Approach

### Team Members:

- Aryaan Khan
- Yuhang Cui

### Description of the Game:

_Five Crowns_ is a card game played with two combined decks of cards, each with values 3 to K and suits Stars, Hearts, Clubs, Spades, and Diamonds, as well as three Jokers (116 cards total). The game is played in epochs that range from 3 to 13, and can be played with 2-7 players.

In each epoch _n_, each player is dealt _n_ cards, and cards of value _n_ are considered 'wild cards'. Each card has a point value, where cards 3 to K have corresponding point values of 3 to 13 points. Jokers are worth 50 points, and wildcards are worth 20 points.

Your hand is scored per the following:
- Runs of 3 or more cards in the same suit count as 0 points.
- Books of 3 or more cards of the same value count as 0 points.
- No overlap allowed between groups of cards.
- Jokers and Wildcards can substitute as any card towards a run or book.

In each epoch, players take turns taking a card from the discard table or drawing a card from the deck to add to their hand. Then, they choose a card from their hand to add to the discard pile. 

At the end of the turn, if the hand is worth 0 points, the player can go out, which means they reveal their hand, and then other players must now also reveal their hands at the end of their turns. The revealed hand scores of all players are tallied up, and the player with the lowest score wins the epoch.


### Programming Approaches:

We made several simplifying assumptions for the game:
- We only deal with epochs 3 to 5 to reduce computation cost
- If the deck run out of cards before anyone goes out, the game ends in a draw
- A player may not take the previous discard and immediately discard it again (Prevents cyclic games)

We implemented 4 agents for the game:
- **Random Agent:**
    - Randomly chooses whether to draw from the deck or the discard pile
    - Randomly chooses a card from their hand to discard
- **Greedy Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Chooses the card to discard that minimizes the score of their hand
- **MCTS Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Randomly guess a deck and player hand configuration, then perform deterministic MCTS using UCT1 with that game state.
- **DQN Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Use Deep Q Network trained for each epoch to decide best discard, with game states encoded as (player hand encoded as count of each card, discard card as one-hot encoding, Go Out status as boolean)
    - Network trained against 3 greedy agents.


### Research Questions

We had two questions in mind as we were implementing this agent:
1. How well does the MCTS agent do against a baseline greedy agent?
    - For an epoch 3 game, MCTS won **54%** of games out of 10,000 games against the greedy agents.
    - For an epoch 4 game, MCTS won **37%** of agmes out of 10,000 games against the greedy agents.
    - For an epoch 5 game, MCTS won **27%** of games out of 10,000 games against the greedy agents.
    - Compared to the reference results of random and greedy players against greedy players, MCTS is much better than random agents, but slightly worse than greedy agents
    - Therefore, we can see that MCTS is very close to a greedy agent's performance for the lowest epoch, but its performance falls tremendously as the game gets more complex.
2. How well does the DQN agent perform against a baseline greedy agent?
    - For an epoch 3 game, DQN won **48%** of games out of 10,000 games against the greedy agents.
    - For an epoch 4 game, DQN won **19%** of games out of 10,000 games against the greedy agents.
    - For an epoch 5 game, DQN won **17%** of games out of 10,000 games against the greedy agents.
    - Compared to reference results of random and greedy players against greedy players, DQN is also noticeably better than random agents, but worse than greedy agents.
    - Therefore, we can conclude that DQN is worse than the greedy agent for effectively all epochs, with epoch 3 being much closer to a greedy agent's performance than the subsequent epochs.

### Limitations

- Due to restricted compute resources and time, the MCTS agents run for 1 second for per move, and the DQN agents are trained for ~2-6 hours, so the performance of these agents may improve with longer runtime or training time.
- Using only epochs 3-5 allows a relatively simple search for books and runs, since only one group of 3 can be in the hand. For larger epochs, scoring each hand is essentially the NP-Complete Knapsack problem, so game execution and scoring time will be much higher.


# Sample Results: {player 1 agent} vs {player 2-4 agent}, 10000 iterations
# For tests to run: Install packages in requirements.txt

====================
Random vs Random:
Game for Epoch 3
Win Rate: 0.304
Average Score: 19.5748
Game for Epoch 4
Win Rate: 0.236
Average Score: 24.3649
Game for Epoch 5
Win Rate: 0.119
Average Score: 29.4691
====================
Random vs Greedy:
Game for Epoch 3
Win Rate: 0.149
Average Score: 25.1951
Game for Epoch 4
Win Rate: 0.051
Average Score: 31.0245
Game for Epoch 5
Win Rate: 0.014
Average Score: 34.7671
====================
Greedy vs Random:
Game for Epoch 3
Win Rate: 0.813
Average Score: 3.3618
Game for Epoch 4
Win Rate: 0.885
Average Score: 1.3393
Game for Epoch 5
Win Rate: 0.9489
Average Score: 0.4931
====================
Greedy vs Greedy:
Game for Epoch 3
Win Rate: 0.552
Average Score: 8.3375
Game for Epoch 4
Win Rate: 0.431
Average Score: 6.8388
Game for Epoch 5
Win Rate: 0.386
Average Score: 5.741
====================
MCTS vs Random:
Game for Epoch 3
Win Rate: 0.791
Average Score: 4.052
Game for Epoch 4
Win Rate: 0.837
Average Score: 2.424
Game for Epoch 5
Win Rate: 0.925
Average Score: 1.0325
====================
MCTS vs Greedy:
Game for Epoch 3
Win Rate: 0.548
Average Score: 9.004
Game for Epoch 4
Win Rate: 0.373
Average Score: 10.528
Game for Epoch 5
Win Rate: 0.274
Average Score: 9.993
====================
DQN vs Random:
Game for Epoch 3
Win Rate: 0.722
Average Score: 7.5549
Game for Epoch 4
Win Rate: 0.705
Average Score: 6.7062
Game for Epoch 5
Win Rate: 0.918
Average Score: 1.587
====================
DQN vs Greedy:
Game for Epoch 3
Win Rate: 0.480
Average Score: 14.5747
Game for Epoch 4
Win Rate: 0.187
Average Score: 19.8691
Game for Epoch 5
Win Rate: 0.172
Average Score: 19.1243
====================