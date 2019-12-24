import torch
from structs.controller import *

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

    def gen_board_tensor(self, board):
        ''' Generates 4th order tensor of current board to train player '''
        out = np.zeros((1, 4, board.board.size+2, board.board.size+2))
        b = board.board.copy()
        b[self.y, self.x, 2] = 0
        out[0, :3, :, :] = b.reshape((3, 20, 20))
        out[0, 3, self.y, self.x] = 1
        return torch.tensor(out, dtype=torch.float)

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
        moveList = board.get_moves((self.y, self.x))
        if len(moveList)==0:
            return False
        if isinstance(self.controller, Bot):
            board = self.gen_board_tensor(board)
        moveChoice = self.controller.choose_move(moveList, board)
        return moveChoice

    def choose_shot(self, board):
        shotChoice = self.controller.choose_shot(board)
        return shotChoice

    def return_to_start(self):
        self.x = self.oX
        self.y = self.oY
