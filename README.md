# Fruit-Ninja-Game-Playing-Agent
This is an implementation of a software agent that can play a zero-sum game against a human or another agent using minimax algorithm and alpha-beta pruning. Also to handle time constraint, used depth limit and children ordering tweaks.

## GAME
The Fruit Ninja is a two player game in which each player tries to maximize his/her share from a batch of fruits randomly placed in a box. The box is divided into cells and each cell is either empty or filled with one fruit of a specific type.

At the beginning of each game, all cells are filled with fruits. Players play in turn and can pick a cell of the box in their own turn and claim all fruit of the same type, in all cells that are connected to the selected cell through horizontal and vertical paths. For each selection or move the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move. Once an agent picks the fruits from the cells, their empty place will be filled with other fruits on top of them (which fall down due to gravity), if any.

In this game, no fruit is added during game play. Hence, players play until all fruits have been claimed. The overall score of each player is the sum of rewards gained for every turn. The game will terminate when there is no fruit left in the box or when a player has run out of time.

We give the best possible state according to our algorithm and print it like column (alphabetical value), row (numeric value) starting from A1.
