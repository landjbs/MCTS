'''
Heavy inspiration from:
https://github.com/int8/monte-carlo-tree-search/blob/master/mctspy/tree/nodes.py
'''

import numpy as np
from collections import defaultdict

class Node(object):
    ''' Node Monte Carlo Tree Search '''
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visitNum = 0
        self.results = defaultdict(int)
        self.unexplored = None

    def load_unexplored(self):
        ''' Load unexplored actions from node '''
        if (self.unexplored == None):
            self.unexplored = self.state.possible_moves()
        return self.unexplored

    def q(self):
        ''' Calcs q value of current state '''
        wins = self.results[self.parent.state.pId]
        losses = self.results[-1 *  self.parent.state.pId]
        return wins - lossesa

    def n(self):
        ''' Returns n value of current state '''
        return self.visitNum

    def expand(self):
        ''' Expand state '''
        a = self.unexplored.pop()
        nextState = self.state.move((a[0], a[1]))
        child = Node(state=nextState, parent=self)
        self.children.append(child)
        return child

    # def is_terminal(self):
    #     return self.

    def policy(self, moves):
        ''' Policy for selecting move from moves during rollout '''


    def rollout(self):
        curState = self.state
        moves = self.state.possible_moves()
        while (len(moves) < 0):
            a =


class MCTS(object):
    ''' Runs a single MCTS from current position on board '''
    def __init__(self, loc, board):
        self.loc = loc
        self.board = board

    def run_search(self):
        moves = self.board.get_moves(self.loc)
        while len(moves) > 0:
            moves = self.board.get_moves(self.loc)

    def choose_max(self, moveList):
        ''' Choose moves with maximal score '''
        pass
