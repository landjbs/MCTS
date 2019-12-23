import numpy as np
from math import floor
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
        print(moveList)
        i = np.random.randint(0, len(moveList))
        return moveList[i]

    def choose_shot(self, board):
        # i = np.random.randint(0, 5)
        return 1
        # return [None, 0, 1, 2, 3][i]


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
        self.x = x
        self.y = y
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
        if len(moveList) == 0:
            return None
        moveChoice = self.controller.choose_move(moveList, board)
        return moveChoice

    def choose_shot(self, board):
        shotChoice = self.controller.choose_shot(board)
        return shotChoice


class Board(object):
    def __init__(self, size, players, cp):
        '''
        Builds board object for laser tag. Stored as third order tensor of shape
        (size, size, 3) where last three dims correspond to shots, walls,
        and players, in that order. Board is low-level object contained in
        higher-level Game object.
        Args:
            size:           Length of one axis of square board.
            players:        List of Player objects for players in game.
            cp:            APPROX wall cover percent of board. Does not account
                            for repetition. If p is 1, entire board
                            will be covered except for edge paths.
        '''
        self.size = size
        self.min = 1
        self.max = size - 2
        self.board = np.zeros((size+2, size+2, 3))
        # add walls
        self.board[0:, 0, 1] = 1
        self.board[0, 0:, 1] = 1
        self.board[0:, size+1, 1] = 1
        self.board[size+1, 0:, 1] = 1
        if (cp == 0):
            pass
        elif (cp == 1):
            self.board[2:size, 2:size, 1] = 1
        elif (0 < cp < 1):
            coverNum = floor(cp * (self.max)**2)
            xCover = np.random.randint(2, self.max, coverNum)
            yCover = np.random.randint(2, self.max, coverNum)
            self.board[yCover, xCover, 1] = 1
        else:
            raise ValueError(f'Expected p in range [0, 1], but found {p}.')
        # add players
        for player in players:
            if self.board[player.y, player.x, 2] == 0:
                self.board[player.y, player.x, 2] = 1
            else:
                raise ValueError('Cannot place two players on the same spot.')

    def get_moves(self, loc):
        ''' Returns list of possible moves from loc '''
        x, y = loc
        minX, maxX = x - 1, x + 2
        minY, maxY = y - 1, y + 2
        kernel = np.sum(self.board[minY:maxY, minX:maxX, 1:], axis=2)
        posMoves = list()
        for i, row in enumerate(kernel):
            for j, elt in enumerate(row):
                if (elt == 0):
                    posMoves.append((j-1, i-1))
        return posMoves

    def move_player(self, newLoc, prevLoc):
        ''' Lossily moves player from prevLoc to newLoc '''
        self.board[prevLoc[0], prevLoc[1], 2] = 0
        self.board[newLoc[0], newLoc[1], 2] = 1

    def clear_shots(self):
        self.board[:, :, 0] = 0

    def add_shot(self, start, d):
        '''
        Adds shot from start in straight line in direction d. Directions are
        1-up, 2-right, 3-down, 4-left. Shots go as far as they can before
        hitting a wall.
        '''
        if (d == 1):
            sliceList = list(self.board[:start[0], start[1], 1])
            sliceList.reverse()
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = max(0, start[0]-wallDist)
            self.board[stop:start[0], start[1], 0] = 1
        elif (d == 2):
            sliceList = list(self.board[start[0], start[1]:, 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = start[1] + wallDist
            self.board[start[0], (start[1]+1):stop, 0] = 1
        elif (d == 3):
            sliceList = list(self.board[start[0]:, start[1], 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = start[0]+wallDist
            self.board[(start[0]+1):stop, start[1], 0] = 1
        elif (d == 4):
            sliceList = list(self.board[start[0], :start[1], 1])
            sliceList.reverse()
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = max(0, start[1]-wallDist)
            self.board[start[0], stop:start[1], 0] = 1
        else:
            raise ValueError(f'Expected d in range [0, 3], but found {d}.')

    def vis(self, show=True, outPath=False):
        plt.imshow(self.board)
        if outPath:
            plt.savefig(outPath)
        if show:
            plt.show()


class Game(object):
    def __init__(self, boardSize, cp, train=True):
        self.p1 = Player(1, 1, Bot('p1'))
        self.p2 = Player(boardSize, boardSize, Dummy('p2'))
        self.board = Board(boardSize, [self.p1, self.p2], cp)
        self.roundCount = 0

    def player_turn(self, p):
        ''' Runs turn for player p. Returns False if they are dead. '''
        if p.is_shot(self.board):
            return False
        move = p.choose_move(self.board)
        if not move:
            return False
        p.move(move[0], move[1], self.board)
        shot = p.choose_shot(self.board)
        if shot:
            print(p.name)
            p.shoot(shot, self.board)
        return True

    def win(self, p):
        ''' Gives winning conditions to player '''
        # if isinstance(p.controller, Bot):
        #     pass
        #     break
        # else:
        #     pass
        print(f'{p.name} is the winner!')

    def play_round(self):
        ''' Plays round returns true if done '''
        if not self.player_turn(self.p1):
            self.win(self.p2)
            return True
        if not self.player_turn(self.p2):
            self.win(self.p1)
            return True
        self.roundCount += 1
        self.board.vis()
        self.board.clear_shots()
        return False

    def play(self, roundNum):
        while (self.roundCount <= roundNum):
            if self.play_round():
                break


x = Game(5, 0)
x.play(100)

# p1 = Player('derek', 0, 0, Bot())
# p2 = Player('landon', 10, 10, Bot())
# x = Board(11, [p1, p2], 1)
# x.vis()
# for i in range(10):
#     mL = p.possible_moves(x)
#     print(mL)
#     m = mL[np.random.randint(0, len(mL))]
#     p.move(m[0], m[1], x)
#     x.vis()
