import random
import copy
import Queue
import math

############################################################
# Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    tile = 1
    board = list()
    for i in xrange(rows):
        board.append([])
        for j in xrange(cols):
            if tile > rows * cols - 1:
                tile = 0
            board[i].append(tile)
            tile += 1
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required

    def __init__(self, board):
        self.board = board
        self.r = len(board)
        self.tile_index_map = {}
        # Avoid index out of range exception
        if self.r != 0:
            self.c = len(board[0])
            for i in xrange(self.r):
                for j in xrange(self.c):
                    if board[i][j] == 0:
                        self.empty_tile = (i, j)
                    self.tile_index_map[board[i][j]] = (i, j)

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        dest_row = 999
        dest_col = 999
        if direction == "up":
            dest_row = self.empty_tile[0] - 1
            dest_col = self.empty_tile[1]
        elif direction == "down":
            dest_row = self.empty_tile[0] + 1
            dest_col = self.empty_tile[1]
        elif direction == "left":
            dest_row = self.empty_tile[0]
            dest_col = self.empty_tile[1] - 1
        elif direction == "right":
            dest_row = self.empty_tile[0]
            dest_col = self.empty_tile[1] + 1
        else:
            return False
        if dest_row < self.r and dest_col < self.c and dest_row >= 0 and dest_col >= 0:
            # print self.empty_tile
            self.board[dest_row][dest_col], self.board[self.empty_tile[0]][self.empty_tile[
                1]] = self.board[self.empty_tile[0]][self.empty_tile[1]], self.board[dest_row][dest_col]
            self.empty_tile = (dest_row, dest_col)
            return True
        else:
            return False

    def scramble(self, num_moves):
        for i in xrange(num_moves):
            direction = random.choice(["up", "left", "right", "down"])
            self.perform_move(direction)

    def is_solved(self):
        temp = create_tile_puzzle(self.r, self.c)
        return temp.board == self.board

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        possible_moves = ["up", "left", "right", "down"]
        for move in possible_moves:
            temp = self.copy()
            if temp.perform_move(move) == True:
                yield (move, temp)

    # Required
    def find_solutions_iddfs(self):
        l = 0
        while True:
            #print "Depth: "
            #print l
            moves = self.iddfs_helper(l)
            if moves:
                break
            else:
                l = l + 1
        for move in moves:
            # s = s[::-1]
            yield move

    def iddfs_helper(self, l):
        stack = []
        stack.append((self,0))
        explored_set = set()
        parent = {}
        parent[self] = self
        moves = {}
        moves[self] = ""
        explored_set.add(tuple(tuple(x) for x in self.get_board()))
        solution = []
        solutions = []
        depth = 0
        if self.is_solved():
            return solutions
        while stack:
            puzzle_instance, depth = stack.pop()
            if depth < l:
                for move, successor in puzzle_instance.successors():
                    if tuple(tuple(x) for x in successor.get_board()) not in explored_set:
                        parent[successor] = puzzle_instance
                        moves[successor] = move
                        if successor.is_solved():
                            node = successor
                            solution = []
                            while(parent[node] != node):
                                solution.append(moves[node])
                                node = parent[node]
                            solutions.append(list(reversed(solution)))
                        else:
                            stack.insert(0,(successor, depth + 1))
                            explored_set.add(tuple(tuple(x)
                                               for x in successor.get_board()))
        return solutions

    # Required
    def find_solution_a_star(self):
        queue = Queue.PriorityQueue()
        explored_set = set()
        parent = {}
        parent[self] = self
        moves = {}
        moves[self] = ""
        goal = create_tile_puzzle(self.r, self.c)
        queue.put((self.h_score(goal), 0, self))
        explored_set.add(tuple(tuple(x) for x in self.get_board()))
        solution = []
        while queue:
            current = queue.get()
            puzzle_instance = current[2]
            g = current[1]
            # print "Parent:"
            # print puzzle_instance.get_board()
            for move, successor in puzzle_instance.successors():
                if tuple(tuple(x) for x in successor.get_board()) not in explored_set:
                    # print "     Child:"
                    # print successor.get_board()
                    parent[successor] = puzzle_instance
                    moves[successor] = move
                    if successor.is_solved():
                        # backtrack through the solution to get the moves
                        node = successor
                        while(parent[node] != node):
                            solution.append(moves[node])
                            node = parent[node]
                        return list(reversed(solution))
                    # add the node to the queue with it's scores and mark it as
                    # explored
                    queue.put(
                        (successor.h_score(goal) + g + 1, g + 1, successor))
                    explored_set.add(tuple(tuple(x)
                                           for x in successor.get_board()))
        return None

    # Get the heuristic manhattan distance between the current board and the
    # goal state
    def h_score(self, goal):
        # calculate distance between self and goal
        man_dist = 0
        for tile in self.tile_index_map:
            man_dist += abs(self.tile_index_map[tile][0] - goal.tile_index_map[tile][0]) + abs(
                self.tile_index_map[tile][1] - goal.tile_index_map[tile][1])
        return man_dist
