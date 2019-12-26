from collections import defaultdict

class Node(object):
    ''' Node Monte Carlo Tree Search '''
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visitNum = 0
        self.results = defaultdict(int)
        self.unexplored = None

    def load_unexplored(self):
        ''' Load unexplored actions from node '''
        if (self.unexplored == None):
            self.unexplored = self.board.get_moves()


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
