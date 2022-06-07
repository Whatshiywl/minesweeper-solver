# Mineswepper Solver
The aim of this project is to attempt to solve a minesweeper game at any point by both identifying mine locations to be flagged and safe locations to be revealed. You can also use it to just play minesweeper on the command line, but frankly, why would you?

## Dependencies
This program only relies on a couple of dependencies:
* [numpy](https://numpy.org/)
* [keyboard](https://pypi.org/project/keyboard/)

## Starting up a game
To start a new game, simply run `sudo python3 src/main.py`. You will be prompted to either enter the desired board dimentions, enter a board file to be loaded or just leave it blank to play with the default values. Dimentions are entered as a comma separated list on the format "rows,cols,mines". For example, entering `30,60,150` would start a board with 30 rows, 60 columns and 150 mines.

The game requires elevated privileges because of the `keyboard` library it depends on to listen to key inputs for an interactive experience. Eventually it could be made such that, if privileges are not conceded, the game still is playable through a more cubbersome mechanic such as inputting the desired actions one by one.

### Board files
At startup, you have the option to pass a valid board file. This is a regular text file containing information about a custom board. It may be used to test specific arrangements to be solved or as a way to distribute challanges. The semantics of the file are as follows:

Each line on the file represents a line on the board. Each line is a list of comma separated tiles. A tile consists of two characters. The first represents the type of the tile, which can be two: A tile without a mine is represented by a number, reflecting the number of mines around it; A tile with a mine is represented by the character 'M'. The second character represents the state of the tile and can take one of three different values: 'H' for a hidden tile, 'V' for a visible tile and 'F' for a flagged tile.

Notice that, because the numbers are being assigned manually, it is possible to create a inconsistent board, meaning the numbers don't reflect the actual number of adjacent mines. If this is the case, the program will inform the first inconsistency it finds and exit so you can fix it. Filling the tile numbers automatically from the mine positions so that writing board files is easier is a planned feature. Allowing an inconsistent board to be played could also be a future feature, if there ever comes a need for it.

An example.mine board file is located in the boards folder. In order to load it, simply input it's location when prompted at startup: `boards/example.mine`

## Playing the game
In case you, for some unknown reason, *really* wants the unprecedented experience of playing minesweeper on the command line and instead of going for a proper engine like [freeweep](http://manpages.ubuntu.com/manpages/trusty/man6/freesweep.6.html) or [MineSweeper](https://github.com/unknownblueguy6/MineSweeper) you decided you wanted to play it with *this*, you can. The number of mines left is displayed at the top, the board shows hidden tiles as blank spaces, visible tiles without adjacent lines are represented as dots, flags are represented as a yellow 'F' and your current position is highlighted in blue. You move around with the `Arrow Keys`, press `Space` to reveal a tile and `F` to toggle a flag on a hidden tile. You can press `Space` on a numbered tile with all adjacent mines flagged to reveal it's remaining hidden neighbours. Your starting position is always in the middle of the board.

## Solving the game
Of course, as stated, the whole purpose of this project is to implement a solver agent for minesweeper and in order to use it, you can press `S` at any moment in the game to have the program play by itself. You can hold down the `S` key if you want fast solving, as the program will only play one action at a time. So you can use this to either solve an entire game from the beginning or to get out of a tight spot.

Note that, since the mines are not yet placed before the first play to guarantee the game won't be lost at the beginning, it makes no sense to run the solver as your first action, so you must choose a starting point to reveal with `Space`.

### How it works
When the solver is invoked during a match, it will look at the current board and generate a system of linear equations based on it. Each equation represents the sum of propabilities of each tile having a mine being equal to the total amount of mines expected for those tiles. The first equation, for example, simply states that the sum of the probabilities of all the currently hidden tiles is equal to the number of mines left, reflecting the fact that you expect the remaining mines to be contained in the set of still hidden tiles.

The other equations are derived for each numbered tile with hidden adjacent mines (if a tile already has all adjacent mines flagged, it is ignored). The program will look at the tile's hidden neighbours and generate an equation reflecting the fact that the remaining number of adjacent mines for that tile must be among it's set of hidden neighbours. For example, if a tile has value 3 and one of it's neighbours is flagged, then there are still 2 mines remaining. If this tile still has 4 hidden neighbours, then the equation will state that the sum of the probabilities of each of those 4 tiles having a mine is 2.

After the system of equations is formulated, it is passed to numpy to find the [least squared solution](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq), which will contain the most likely probabilities for each of the hidden tiles. Any tile with a probability greater than 1 is considered as having a mine and any probability lower than 0 indicates no mines. Since this is a least squared solution, values are aproximates and a precision of 1e-6 is used such that values lower than but close to 1 are considered as being 1 and values higher than but close to 0 are considered as being 0.

The solver agent will first try to place flags. It will filter the solution for tiles which it thinks has mines on them and pick one at random to flag. If none of these exist, it will instead look for tiles which it thinks has no mines. It will once again pick one of those at random and reveal it.

If none of the above conditions are met, the solver agent will do nothing. This can happen because [not all minesweeper boards are solvable](https://www.quora.com/Are-all-Minesweeper-games-solvable) with the information given and sometimes it can come down to sheer luck. In these cases, the solver will not take a guess and the player must act on their own.

Notice that the solver does not have knownledge of the actal positions of the mines and only uses the information available to the player to find the best solution. It also plays as the player, meaning that it is possible for it to lose a game. This most likely will happen in case the player misplaces a flag. Since the solver has no way of knowing if there really is a mine on the flagged tile, it will assume there is and this could (and in fact always would) lead to the solver ultimately making a wrong move.

It is also possible for the solver to lose a game it has played entirely on it's own or one which has all the flags placed correctly. This mainly happens on bigger boards and is likely due to the fact that, with more tiles, the probabilities are more spread out and thus have lower values, requiring a stricter precision than the one used. However, the real reason why the solver sometimes loses on it's own and under which circumstances this tends to happen are not very clear for me at the moment and any theories and/or fixes would be very welcome!
