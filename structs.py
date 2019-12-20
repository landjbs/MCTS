import numpy as np
from math import floor
import matplotlib.pyplot as plt

class Player(object):
    def __init__(self, name):
        pass

class Board(object):
    def __init__(self, size, coverPercent):
        self.board = np.zeros((size, size, 3))
        coverNum = floor(coverPercent * size**2)
        coverLocs = set([(0,0), (size, size)])
        while len(coverLocs) < coverNum:
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)
            if not (x, y) in coverLocs:
                self.board[x, y, 1] = 1
                coverLocs.add((x, y))

    def visualize(self, show=True, outPath=False):
        plt.imshow(self.board)
        if outPath:
            plt.savefig(outPath)
        if show:
            plt.show()

x = Board(10, 0.1)
x.visualize()
