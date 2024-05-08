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

At the end of the turn, if the hand is worth 0 points, the player can Go Out, which means they reveal their hand, and then other players must now also reveal their hands at the end of their turns. The revealed hand scores of all players are tallied up, and the player with the lowest score wins the epoch.


### Programming Approaches:

We made several simplifying assumptions for the game:
- We only deal with epochs 3 to 5 to reduce computation cost
- If the deck run out of cards before anyone Go Out, the game ends in a draw
- A player may not take the previous discard and immediately discard it again (Prevents cyclic g)

We implemented 4 agents for the game:
- **Random Agent:**
    - Randomly chooses whether to draw from the deck or the discard pile
    - Randomly chooses a card from their hand to discard
- **Greedy Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Chooses the card to discard that minimizes the score of their hand
- **MCTS Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Randomly guess a deck and player hand configuration, then perform deterministic MCTS with that game state.
- **DQN Agent:**
    - Chooses the action (draw from deck or discard) that minimizes the expected score of their hand
    - Use Deep Q Network trained for each epoch to decide best discard.
    - Network trained against 3 greedy agents.


### Research Question

We had two questions as we were implementing this agent:
1. How well does the MCTS agent do against a baseline greedy agent?
2. How well does the DQN agent perform against a baseline greedy agent?