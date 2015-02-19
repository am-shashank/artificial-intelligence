############################################################
# Dominoes Game
############################################################

import random
import copy
import Queue
import math

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for i in range(cols)] for j in range(rows)])


class DominoesGame(object):

    # global variable
    leaf_nodes = 0

    # Required

    def __init__(self, board):
        self.board = board
        self.r = len(board)
        if self.r != 0:
            self.c = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for i in range(self.c)] for j in range(self.r)]

    # check if move is within bounds of board and if the cells are actually
    # empty
    def is_legal_move(self, row, col, vertical):
        if vertical is True:
            if row < self.r - 1 and col < self.c:
                if self.board[row][col] == False and self.board[row + 1][col] == False:
                    return True
                else:
                    return False
            else:
                return False
        else:
            if row < self.r and col < self.c - 1:
                if self.board[row][col] == False and self.board[row][col + 1] == False:
                    return True
                else:
                    return False
            else:
                return False

    def legal_moves(self, vertical):
        for i in xrange(self.r):
            for j in xrange(self.c):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    # assume that it's a legal move
    def perform_move(self, row, col, vertical):
        if vertical is True:
            self.board[row][col] = True
            self.board[row + 1][col] = True
        else:
            self.board[row][col] = True
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        for (i, j) in self.legal_moves(vertical):
            return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            temp = self.copy()
            temp.perform_move(move[0], move[1], vertical)
            yield (move, temp)

    def get_random_move(self, vertical):
        return random.choice(self.legal_moves(vertical))

    def evaluate_board(self, root):
        return len(list(self.legal_moves(root))) - len(list(self.legal_moves(not root)))

    def alpha_beta_search(self, depth, alpha, beta, vertical, root, maxPlayer):
        if depth == 0 or self.game_over(vertical):
            DominoesGame.leaf_nodes = DominoesGame.leaf_nodes + 1
            return ((0,0), self.evaluate_board(root))
        if maxPlayer:
            v = float("-inf")
            required_move = tuple()
            for move, child in self.successors(vertical):
                position, temp = child.alpha_beta_search(depth - 1, alpha, beta, not vertical, root, False)
                if temp > v:
                    v = temp
                    required_move = move
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return (required_move, v)
        else:
            v = float("inf")
            required_move = tuple()
            for move, child in self.successors(vertical):
                position, temp = child.alpha_beta_search(depth - 1, alpha, beta, not vertical, root, True)
                if temp < v:
                    v = temp
                    required_move = move
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return (required_move, v)
            
    # Required
    def get_best_move(self, vertical, limit):
        move, value = self.alpha_beta_search(limit, float("-inf"), float("inf"), vertical, vertical, True)
        temp = DominoesGame.leaf_nodes
        DominoesGame.leaf_nodes = 0
        return move, value, temp
