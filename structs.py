import numpy as np
from math import floor
import matplotlib.pyplot as plt


class Player(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def move(self, nX, nY, board):
        board.move_player((nY, nX), (self.y, self.x))
        self.x = nX
        self.y = nY

    def shoot(self, d, board):
        board.add_shot((self.y, self.x), d)

    def possible_moves(self, board):
        localKernel = board.board[(self.y-1):(self.y+1), (self.x-1):(self.x+1)]
        print(localKernel)


class Board(object):
    def __init__(self, size, p):
        '''
        Builds board object for laser tag. Stored as third order tensor of shape
        (size, size, 3) where last three dims correspond to shots, walls,
        and players, in that order. Board is low-level object contained in
        higher-level Game object.
        Args:
            size:           Length of one axis of square board
            p:              APPROX wall cover percent of board. Does not account
                            for repetition. If p is 1, entire board
                            will be covered except for edge paths.
        '''
        self.size = size
        self.max = size - 1
        self.board = np.zeros((size, size, 3))
        # add walls
        if (p == 0):
            pass
        elif (p == 1):
            self.board[1:self.max, 1:self.max, 1] = 1
        elif (0 < p < 1):
            coverNum = floor(p * (self.max)**2)
            xCover = np.random.randint(1, self.max, coverNum)
            yCover = np.random.randint(1, self.max, coverNum)
            self.board[yCover, xCover, 1] = 1
        else:
            raise ValueError(f'Expected p in range [0, 1], but found {p}.')
        # add players
        self.board[[0, self.max], [0, self.max], 2] = 1

    def get_moves(self, loc):
        ''' Returns list of possible moves at loc '''
        self.board

    def move_player(self, newLoc, prevLoc):
        ''' Lossily moves player from prevLoc to newLoc '''
        self.board[prevLoc[0], prevLoc[1], 2] = 0
        self.board[newLoc[0], newLoc[1], 2] = 1

    def clear_shots(self):
        self.board[:, :, 0] = 0

    def add_shot(self, start, d):
        '''
        Adds shot from start in straight line in direction d. Directions are
        0 - up, 1 - right, 2 - down, 3 - left. Go as far as they can before
        hitting a wall.
        '''
        if (d == 0):
            sliceList = list(self.board[:start[0], start[1], 1])
            sliceList.reverse()
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = max(0, start[0]-wallDist)
            self.board[stop:start[0], start[1], 0] = 1
        elif (d == 1):
            sliceList = list(self.board[start[0], start[1]:, 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = start[1] + wallDist
            self.board[start[0], (start[1]+1):stop, 0] = 1
        elif (d == 2):
            sliceList = list(self.board[start[0]:, start[1], 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = start[0]+wallDist
            self.board[(start[0]+1):stop, start[1], 0] = 1
        elif (d == 3):
            sliceList = list(self.board[start[0], :start[1], 1])
            sliceList.reverse()
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = max(0 , start[1]-wallDist)
            self.board[start[0], stop:start[1], 0] = 1
        else:
            raise ValueError(f'Expected d in range [0, 3], but found {d}.')

    def vis(self, show=True, outPath=False):
        plt.imshow(self.board)
        if outPath:
            plt.savefig(outPath)
        if show:
            plt.show()


# class Game(object):
#     def __init__(self, )


x = Board(11, 0.1)
p = Player('derek', 0, 0)
p.shoot(2, x)
# x.vis()
x.clear_shots()
p.move(1, 0, x)
# x.vis()
print(p.possible_moves(x))
# x.move_player((5,5), (0,0))
# for i in range(4):
#     x.add_shot((5, 5), i)
#     x.vis()
