import numpy as np
from math import floor
import matplotlib.pyplot as plt

class Player(object):
    def __init__(self, name):
        pass

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
                wallDist = sliceList.index(1)
            except ValueError:
                wallDist = self.max
            stop = max(0, start[0]-(wallDist+1))
            self.board[stop:start[0], start[1], 0] = 1
        elif (d == 1):
            sliceList = list(self.board[start[0], start[1]:, 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            self.board[start[0], (start[1]+1):wallDist, 0] = 1
        elif (d == 2):
            sliceList = list(self.board[start[0]:, start[1], 1])
            try:
                wallDist = sliceList.index(1) + 1
            except ValueError:
                wallDist = self.size
            stop = min(self.size, start[0]+wallDist)
            self.board[(start[0]+1):stop, start[1], 0] = 1
        elif (d == 3):
            sliceList = list(self.board[:start[0], start[1], 1])
            
        else:
            raise ValueError(f'Expected d in range [0, 3], but found {d}.')

    def vis(self, show=True, outPath=False):
        plt.imshow(self.board)
        if outPath:
            plt.savefig(outPath)
        if show:
            plt.show()


x = Board(10, 0.3)
x.add_shot((0, 9), 2)
x.vis()
