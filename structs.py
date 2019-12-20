import numpy as np
from math import floor
import matplotlib.pyplot as plt

class Player(object):
    def __init__(self, name):
        pass

class Board(object):
    def __init__(self, size, coverPercent):
        '''
        Builds board object
        Args:
            size:           Length of one axis of square board
            coverPercent:   APPROX wall cover percent of board. Does not account
                            for repetition. If cover percent is 1, entire board
                            will be covered except for edge paths.
        '''
        self.board = np.zeros((size, size, 3))
        # add walls
        coverNum = floor(coverPercent * (size-1)**2)
        xCover = np.random.randint(1, size-1, coverNum)
        yCover = np.random.randint(1, size-1, coverNum)
        self.board[xCover, yCover, 1] = 1
        # add players
        self.board[[0,size-1], [0, size-1], 2] = 1

    def visualize(self, show=True, outPath=False):
        plt.imshow(self.board)
        if outPath:
            plt.savefig(outPath)
        if show:
            plt.show()

x = Board(10, 1)
x.visualize()
