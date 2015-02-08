#N-Queens
In this section, you will develop a solver for the n-queens problem, wherein n queens are to be placed on
an n × n chessboard so that no pair of queens can attack each other. Recall that in chess, a queen can attack
any piece that lies in the same row, column, or diagonal as itself.

1. Rather than performing a search over all possible placements of queens on the board, it
is sufficient to consider only those configurations for which each row contains exactly one queen.
Without taking any of the chess-specific constraints between queens into account, implement the pair
of functions num_placements_all(n) and num_placements_one_per_row(n) that return the number
of possible placements of n queens on an n × n board without or with this additional restriction.
Think carefully about why this restriction is valid, and note the extent to which it reduces the size of
the search space. You should assume that all queens are indistinguishable for the purposes of your
calculations.

2. With the answer to the previous question in mind, a sensible representation for a board
configuration is a list of numbers between 0 and n − 1, where the ith number designates the column
of the queen in row i for 0 ≤ i < n. A complete configuration is then specified by a list containing
n numbers, and a partial configuration is specified by a list containing fewer than n numbers. Write
a function n_queens_valid(board) that accepts such a list and returns True if no queen can attack
another, or False otherwise. Note that the board size need not be included as an additional argument
to decide whether a particular list is valid.

>>> n_queens_valid([0, 0])
False
>>> n_queens_valid([0, 2])
True
>>> n_queens_valid([0, 1])
False
>>> n_queens_valid([0, 3, 1])
True


3. Write a function n_queens_solutions(n) that yields all valid placements of n queens
on an n × n board, using the representation discussed above. The output may be generated in any
order you see fit. Your solution should be implemented as a depth-first search, where queens are
successively placed in empty rows until all rows have been filled. Hint: You may find it helpful to
define a helper function n_queens_helper(n, board) that yields all valid placements which extend
the partial solution denoted by board.
Though our discussion of search in class has primarily covered algorithms that return just a single
solution, the extension to a generator which yields all solutions is relatively simple. Rather than using
a return statement when a solution is encountered, yield that solution instead, and then continue
the search.

>>>solutions = n_queens_solutions(4)
>>>next(solutions)
[1,3, 0, 2]
next(solutions)
[2,0, 3, 1]

#Lights Out Puzzle
The Lights Out puzzle consists of an m × n grid of lights, each of which has two states: on and off. The
goal of the puzzle is to turn all the lights off, with the caveat that whenever a light is toggled, its neighbors
above, below, to the left, and to the right will be toggled as well. If a light along the edge of the board is
toggled, then fewer than four other lights will be affected, as the missing neighbors will be ignored.
In this section, you will investigate the behavior of Lights Out puzzles of various sizes by implementing a
LightsOutPuzzle class. Once you have completed the problems in this section, you can test your code in
an interactive setting using the provided GUI. See the end of the section for more details.
1. [2 Points] A natural representation for this puzzle is a two-dimensional list of Boolean values, where
True corresponds to the on state and False corresponds to the off state. In the LightsOutPuzzle
class, write an initialization method __init__(self, board) that stores an input board of this form
for future use. Also write a method get_board(self) that returns this internal representation. You
additionally may wish to store the dimensions of the board as separate internal variables, though this
is not required.
>>> b = [[True, False], [False, True]]
>>> p = LightsOutPuzzle(b)
>>> p.get_board()
[[True, False], [False, True]]
