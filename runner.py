import numpy as np
from math import floor, ceil
import matplotlib.pyplot as plt


class Controller(object):
    def __init__(self, name):
        self.name = name

    def choose_move(self, moveList, board):
        pass

    def choose_shot(self, board):
        pass


class Human(Controller):
    ''' Human-controlled player for game api # TODO: finish '''
    def __init__(self, name):
        super(Human, self).__init__(name)

    def choose_move(self, moveList, board):
        pass

    def choose_shot(self, board):
        pass


class Bot(Controller):
    ''' Bot-controlled player that learns across games '''
    def __init__(self, name):
        super(Bot, self).__init__(name)

    def choose_move(self, moveList, board):
        i = np.random.randint(0, len(moveList))
        return moveList[i]

    def choose_shot(self, board):
        i = np.random.randint(0, 5)
        return [0, 1, 2, 3, 4][i]


class Dummy(Controller):
    ''' Dummy player that stays in one spot and never shoots '''
    def __init__(self, name):
        super(Dummy, self).__init__(name)

    def choose_move(self, moveList, board):
        return (0, 0)

    def choose_shot(self, board):
        return None


class Player(object):
    ''' Base player class to be inherited by Human and Bot '''
    def __init__(self, x, y, controller):
        self.name = controller.name
        # updating loc
        self.x = x
        self.y = y
        # perpetual spawn loc
        self.oX = x
        self.oY = y
        self.controller = controller

    def move(self, dx, dy, board):
        nX, nY = self.x + dx, self.y + dy
        board.move_player((nY, nX), (self.y, self.x))
        self.x = nX
        self.y = nY

    def shoot(self, d, board):
        board.add_shot((self.y, self.x), d)

    def possible_moves(self, board):
        return board.get_moves((self.x, self.y))

    def is_shot(self, board):
        ''' Player checks if it is on laser '''
        return (board.board[self.y, self.x, 0] == 1)

    def choose_move(self, board):
        moveList = self.possible_moves(board)
        print(moveList)
        if len(moveList) == 0:
            return None
        moveChoice = self.controller.choose_move(moveList, board)
        return moveChoice

    def choose_shot(self, board):
        shotChoice = self.controller.choose_shot(board)
        return shotChoice

    def return_to_start(self):
        self.x = self.oX
        self.y = self.oY


bSize = 3
p1 = Player(1, 1, Bot('p1'))
p2 = Player(bSize, bSize, Bot('p2'))
p3 = Player(1, bSize, Bot('p3'))
p4 = Player(bSize, 1, Bot('p4'))

for _ in range(1):
    x = Game([p1, p2, p3, p4], bSize, 0)
    x.board.vis()
    x.play(1000)
