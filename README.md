# Fighting the Landlord with Monte Carlo Simulation
***
## Quick Start
Simply download the 5 .py modules and the .ipynb notebook.
Run main.py first to get the data (.csv) file for analysis.
(Or get it from the repo in /data; remember to place it in the same directory as the jupyter notebook)
The data files are used in the Result_Analysis.ipynb for analysis.

Notes: There are some modifiable arguments in the main.py:
- rules: A list of different rules for the game
  - ORIGINAL: The original rule
  - SPECIAL1: 2 with 1 move is added
  - SPECIAL2: 2 pairs with 1 move is added
  - SPECIAL3: The landlord plays an additional move before the game
- games: How many games a simulation should play
- landlord_lv: Level_of_landlord, ranged from 0-9
- peasants_lv: Level_of_peasants, ranged from 0-9
- single_sim:
  - True: Runs only a specific level of landlord and peasants
  - False: Runs all level combinations of landlord and peasants
- print_details:
  - True: Prints the detail of each game, including the moves players played,
    the hand of players, moves played in a round
  - False: Prints only the win rates and runtime of each simulation
- write_file:
  - True: Writes .csv files to the directory
  - False: Does not write files
***
## Introduction
[**Fighting the Landlord**](https://en.wikipedia.org/wiki/Dou_dizhu) (斗地主, Dou DiZhu) is a game that is played with Poker cards with Jokers included.
There are three people in a game: one landlord and two peasants as a team.
Everyone is dealt 17 shuffled cards before the role assignment.
Players bid to be the landlord, who gets the remaining three cards shown to all players.
The **objective** of the game is to **play all the cards** on hand to win!
***
## Program Designing
### Objects (objects.py)
#### Deck
A deck has two attributes:
- Points: Used for bidding the landlord; better cards have higher points
- Cards: A list that contains all cards in the deck, the point system is:
  - 3~A are 3~14, 2 is 16
  - Small King (black Joker) is 20
  - Big King (colored Joker) is 30


#### Player
A player has five attributes:
- Character: Landlord, Peasant 1, and Peasant 2 are assigned with different integers
- Hand: The cards a player has on the hand
- Hand points: Sum up the hand of a player for bidding the landlord
- First player next round: True if the player plays first the next round
- Strength: How strong a player plays ranged from 0 to 9, where 9 is the most aggressive
### Moves (game_moves.py)
- A move detector function
- A move generation class

Legal moves:

- Single: A single card, e.g. [3]
- Pair: Two identical cards, e.g. [3, 3]
- Triple: Three identical cards, e.g. [3, 3, 3]
- Bomb: Four identical cards, e.g. [3, 3, 3, 3]
- King bomb: Two Jokers, i.e. [20, 30]
- Triple with one: E.g. [3, 3, 3, 4]
- Triple with pair: E.g. [3, 3, 3, 4, 4]
- Serial single: E.g. [3, 4, 5, 6, 7], min length: 5, max length: 3 to A
- Serial pair: E.g. [3, 3, 4, 4, 5, 5], min length: 3
- Serial triple: E.g. [3, 3, 3, 4, 4, 4], min length: 2
- Serial triple with one (plane): E.g. [3, 3, 3, 4, 4, 4, 5, 6], min length: 2
- Serial triple with pair (plane): E.g. [3, 3, 3, 4, 4, 4, 5, 5, 6, 6], min length: 2
- Four with two: E.g. [3, 3, 3, 3, 4, 5]
- Four with two pairs: E.g. [3, 3, 3, 3, 4, 4, 5, 5]

Added moves (special rule):
- Pair with one: E.g. [3, 3, 4]
- Two pairs with one: E.g. [3, 3, 4, 4, 5]
### Game Functions (game_functions.py)
Include functions for dealing cards, playing cards, checking if a winner exists, etc.
***
## Validation of the Simulation
- The distribution of the points a landlord gets
- Landlord Win Rates for different playing strength

See [Result_Analysis](https://github.com/50206richie/DouDiZhu-with-Monte-Carlo-Simulation/blob/main/Result_Analysis.ipynb) for more details
***
## Experiments
### Experiment 1
Difference when the game rule "Pair with one" is added
### Experiment 2
Difference when the game rule "Two pairs with one" is added
### Experiment 3
Difference when the game rule "Landlord plays an additional move before the game" is added

See [Result_Analysis](https://github.com/50206richie/DouDiZhu-with-Monte-Carlo-Simulation/blob/main/Result_Analysis.ipynb) for more details
## Summary
- The game design was more complicated than I thought, let alone doing deep learning on it.
- In validation, we observed that the randomness of hand points has convergence.
- The experiment of adding new rules made little impact on the win rates.
  Consider making up another rule that is really different from the original to observe the difference between them.
## Future Works
- Find out what functions occupy the most time and do enhancement, e.g. multiprocessing.
- Maybe consider adding functions that make players record previous moves by all players.
## References
1. [Zha, Daochen et al. “DouZero: Mastering DouDizhu with Self-Play Deep Reinforcement Learning.” ICML (2021)
](https://github.com/kwai/DouZero)
   - Move generation and detection
2. Demo files (poker.py, my_lib.py) from "Programming for Business Computing" 2023 Spring at National Taiwan University
   - Classes of Deck and Player
3. ChatGPT
   - Sample functions testing
