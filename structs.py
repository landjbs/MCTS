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
        coverXs, coverYs = set(), set()
        while len(coverLocs) < coverBlocks:
            coverXs.add(np.random.randint(0, size))
            coverYs.add(np.random.randint(0, size))

    def visualize(self):
        plt.imshow(self.board)
        plt.show()
