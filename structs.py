import numpy as np
import matplotlib.pyplot as plt

class Player(object):
    def __init__(self, name):
        pass

class Board(object):
    def __init__(self, size):
        self.board = np.zeros((size, size, 3))
        

    def visualize(self):
        plt.imshow(self.board)
        plt.show()
