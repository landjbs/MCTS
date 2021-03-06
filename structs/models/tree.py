'''
Heavily inspired by:
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

    def fully_explored(self):
        ''' Checks if current state is fully explored '''
        return (len(self.unexplored)==0)

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
        nextState = self.state.move(a[0], a[1])
        child = Node(state=nextState, parent=self)
        self.children.append(child)
        return child

    def policy(self, moves):
        ''' Policy for selecting move from moves during rollout '''
        return moves[np.random.randint(0, len(moves))]

    def rollout(self):
        ''' Performs rollout from current state until leaf is reached '''
        curState = self.state
        moves = self.state.possible_moves()
        while (len(moves) < 0):
            a = self.policy(moves)
            curState = curState.move(a[0], a[1])
            moves = curState.possible_moves()

    def backprop(self, r):
        ''' Backprops result r through tree '''
        self.visitNum += 1
        self.results[r] += 1
        if self.parent:
            self.parent.backprop(r)

    def best_child(self, a=1.4):
        ''' Chooses best child in children list using formula and param a '''
        # pick weights for children
        weights = [(c.q / c.n) + a * np.sqrt((2 * np.log(self.n) / c.n))
                    for c in self.children]
        # choose best child
        return self.children(np.max(weights))


class Search(object):
    ''' Runs search of MCTS built from nodes '''
    def __init__(self, node):
        self.root = node

    def tree_policy(self):
        ''' Policy for selecting nodes for rollout '''
        curNode = self.root
        while (self.node.possible_moves != None):
            if not curNode.fully_explored():
                return curNode.expand()
            else:
                curNode = curNode.best_child()
        return curNode

    def choose_action(self, n):
        ''' Chooses best action for n simulations '''
        for _ in range(n):
            # choose node
            v = self.tree_policy()
            # perform rollout and backprop action
            reward = v.rollout()
            v.backprop(reward)
        return self.root.best_child(a=0)


# class MCTS(object):
#     ''' Runs a single MCTS from current position on board '''
#     def __init__(self, loc, board):
#         self.loc = loc
#         self.board = board
#
#     def run_search(self):
#         moves = self.board.get_moves(self.loc)
#         while len(moves) > 0:
#             moves = self.board.get_moves(self.loc)
#
#     def choose_max(self, moveList):
#         ''' Choose moves with maximal score '''
#         pass
