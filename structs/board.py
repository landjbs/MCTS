import numpy as np
from math import floor, ceil
import matplotlib.pyplot as plt


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
        self.max = size - 1
        self.board = np.zeros((size+2, size+2, 3))
        # add walls
        # TODO: add rules such that mandated size scales with player number
        if (size > 3):
            pass
        elif (size == 3):
            if cp not in [0, 1]:
                raise ValueError('Boards with size 3 must have cp in [0, 1].')
        else:
            raise ValueError('size must be greater than 3.')
        self.board[0:, 0, 1] = 1
        self.board[0, 0:, 1] = 1
        self.board[0:, size+1, 1] = 1
        self.board[size+1, 0:, 1] = 1
        if (cp == 0):
            pass
        elif (cp == 1):
            self.board[2:size, 2:size, 1] = 1
        elif (0 < cp < 1):
            coverNum = floor(cp * (self.size)**2)
            xCover = np.random.randint(2, self.size, coverNum)
            yCover = np.random.randint(2, self.size, coverNum)
            self.board[yCover, xCover, 1] = 1
        else:
            raise ValueError(f'Expected cp in range [0, 1], but found {cp}.')
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

    def remove_player(self, loc):
        self.board[loc[1], loc[0], 2] = 0

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
