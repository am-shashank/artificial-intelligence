#Tile Puzzle

The Eight Puzzle consists of a 3 × 3 board of sliding tiles with a single empty space.
For each configuration, the only possible moves are to swap the empty tile with one of its neighboring tiles.
The goal state for the puzzle consists of tiles 1-3 in the top row, tiles 4-6 in the middle row, and tiles 7 and 8
in the bottom row, with the empty space in the lower-right corner.
In this section, you will develop two solvers for a generalized version of the Eight Puzzle, in which the
board can have any number of rows and columns.

A natural representation for this puzzle is a two-dimensional list of integer values between 0 and r · c − 1
(inclusive), where r and c are the number of rows and columns in the board, respectively. In this problem,
we will adhere to the convention that the 0-tile represents the empty space.
