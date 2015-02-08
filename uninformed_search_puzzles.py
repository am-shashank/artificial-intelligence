############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy
import math

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return f(n*n) / f(n) / f(n*n-n)

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    #main idea - difference between rows and columns are same
    pawn_column_row = {}
    ctr = 0
    for column in board:
    	#queen in same column
        if column in pawn_column_row:
            return False
        else:
   	    #queen in diagonal column
            for c,r in pawn_column_row.iteritems():
                if abs(c - column) == abs(r - ctr):
                    return False
                pawn_column_row[column] = ctr
        ctr += 1
    return True


def n_queens_solutions(n):
    solutions = [[]]
    for row in xrange(n):
        solutions = (solution+[i] for solution in solutions for i in xrange(n) if n_queens_valid(solution+[i]))
    return solutions
############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        #get number of rows and columns
        maxRow = len(self.board)
        maxCol = 0
    	#avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        self.board[row][col] = not self.board[row][col]
        if row-1 >= 0:
            self.board[row-1][col] = not self.board[row-1][col]
        if col-1 >= 0:
            self.board[row][col-1] = not self.board[row][col-1]
        if col+1 < maxCol:
            self.board[row][col+1] = not self.board[row][col+1]
        if row+1 < maxRow:
            self.board[row+1][col] = not self.board[row+1][col]

    def scramble(self):
        maxRow = len(self.board)
        maxCol = 0
        #avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        for row in xrange(maxRow):
            for col in xrange(maxCol):
                if random.random() < 0.5:
                    self.perform_move(row,col)

    def is_solved(self):
        for row in self.board:
            for switch in row:
                if switch:
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        maxRow = len(self.board)
        maxCol = 0
        #avoid index out of range exception for empty boards
        if maxRow >= 0:
            maxCol = len(self.board[0])
        for row in xrange(maxRow):
            for col in xrange(maxCol):
                successor = self.copy()
                successor.perform_move(row,col)
                yield ((row,col),successor)

    def find_solution(self):
        explored_set = set()
        q = []
        parent = {}
        moves = {}
        parent[self] = self
        moves[self] = (0,0)
        #final solution containing the appropriate moves
        solution = []
        if self.is_solved():
            return moves[self]
        q.append(self)
        explored_set.add(tuple(tuple(x) for x in self.get_board()))
        while len(q) != 0:
            puzzleInstance = q.pop(0)
            if puzzleInstance.is_solved():
                    node = puzzleInstance
                    while(parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
            for move, neighbor in puzzleInstance.successors():
                if tuple(tuple(x) for x in neighbor.get_board()) not in explored_set:
                    parent[neighbor] = puzzleInstance
                    moves[neighbor] = move
                    if neighbor.is_solved():
                        node = neighbor
                        while(parent[node] != node):
                            solution.append(moves[node])
                            node = parent[node]
                        return list(reversed(solution))
                    q.append(neighbor)
                    explored_set.add(tuple(tuple(x) for x in neighbor.get_board()))
        return None

def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for i in xrange(cols)] for j in xrange(rows)])

############################################################
# Section 3: Linear Disk Movement
############################################################

class DiskMovement(object):
    def __init__(self, disks, length, n):
        self.disks = list(disks)
        self.length = length
        self.n = n

    def successors(self):
        i = 0
        li = self.disks
        while i < len(self.disks):
            if li[i] != 0:
                if i + 1 < self.length:
                    if li[i+1] == 0:
                        temp = list(self.disks)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i+1] = disk_to_move
                        yield((i, i+1), DiskMovement(temp,self.length,self.n))
                if i + 2 < self.length:
                    if li[i+2] == 0 and li[i+1] !=0:
                        temp = list(self.disks)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i+2] = disk_to_move
                        yield((i, i+2), DiskMovement(temp,self.length,self.n))
                if i-1 >= 0:
                    if li[i-1] == 0:
                        temp = list(self.disks)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i-1] = disk_to_move
                        yield((i, i-1), DiskMovement(temp,self.length,self.n))
                if i - 2 >= 0:
                    if li[i-2] == 0 and li[i-1] !=0:
                        temp = list(self.disks)
                        disk_to_move = temp[i]
                        temp[i] = 0
                        temp[i-2] = disk_to_move
                        yield((i, i-2), DiskMovement(temp,self.length,self.n))
            i += 1

def is_solved_identical(dm):
    i = dm.length - 1
    while i >= dm.length - dm.n:
        if dm.disks[i] != 1:
            return False
        i -= 1
    return True

def solve_identical_disks(length, n):
    #Disk numbers starting from 1
    initialDisks = [1 for i in xrange(n)]
    #fill empty slots with 0
    for i in xrange(length - n):
        initialDisks.append(0)
    dm = DiskMovement(initialDisks, length, n)
    moves = {}
    parent = {}
    explored_set = set()
    solution = []
    parent[dm] = dm
    moves[dm] = ()
    q = []
    q.append(dm)
    explored_set.add(tuple(dm.disks))
    if is_solved_identical(dm):
        return moves[dm]
    while len(q)!= 0:
        diskInstance = q.pop(0)
        if is_solved_identical(diskInstance):
            node = diskInstance
            while(parent[node] != node):
                solution.append(moves[node])
                node = parent[node]
            return list(reversed(solution))
        for move, neighbor in diskInstance.successors():
            if tuple(neighbor.disks) not in explored_set:
                parent[neighbor] = diskInstance
                moves[neighbor] = move
                if is_solved_identical(neighbor) is True:
                    node = neighbor
                    while(parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
                explored_set.add(tuple(neighbor.disks))
                q.append(neighbor)
    return None
    
def is_solved_distinct(dm):
        i = len(dm.disks) - 1
        diskId = 1
        while diskId <= dm.n:
            if dm.disks[i] != diskId:
                return False
            i -= 1
            diskId += 1
        return True

def solve_distinct_disks(length, n):
    #Disk numbers starting from 1
    initialDisks = [i+1 for i in xrange(n)]
    #fill empty slots with 0
    for i in xrange(length - n):
        initialDisks.append(0)
    dm = DiskMovement(initialDisks, length, n)
    moves = {}
    parent = {}
    explored_set = set()
    solution = []
    parent[dm] = dm
    moves[dm] = ()
    q = []
    if is_solved_distinct(dm):
        return moves[dm]
    q.append(dm)
    explored_set.add(tuple(dm.disks))
    while len(q) != 0:
        diskInstance = q.pop(0)
        if is_solved_distinct(diskInstance):
            node = diskInstance
            while(parent[node] != node):
                solution.append(moves[node])
                node = parent[node]
            return list(reversed(solution))
        for move, neighbor in diskInstance.successors():
            if tuple(neighbor.disks) not in explored_set:
                parent[neighbor] = diskInstance
                moves[neighbor] = move
                if is_solved_distinct(neighbor):
                    node = neighbor
                    while(parent[node] != node):
                        solution.append(moves[node])
                        node = parent[node]
                    return list(reversed(solution))
                q.append(neighbor)
                explored_set.add(tuple(neighbor.disks))
    return None
