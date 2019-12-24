import numpy as np
import torch
from structs.board import Board


class Game(object):
    def __init__(self, pList, boardSize, cp):
        self.pList = pList
        self.board = Board(boardSize, pList, cp)
        self.roundCount = 0
        self.historyTensor = np.expand_dims(np.copy(self.board.board), axis=2)

    def add_history(self):
        self.historyTensor = np.concatenate([self.historyTensor,
                                             self.board.board], axis=2)

    def gen_train_tensor(self, p):
        ''' Generates 4th order tensor of current board to train player p '''
        out = np.zeros((1, 4, self.board.size+2, self.board.size+2))
        b = self.board.board.copy()
        b[p.y, p.x, 2] = 0
        out[0, :3, :, :] = b.reshape((3, 20, 20))
        out[0, 3, p.y, p.x] = 1
        return torch.tensor(out)

    def player_turn(self, p):
        ''' Runs turn for player p. Kills them if they can't move '''
        move = p.choose_move(self.board)
        if not move:
            self.lose(p)
        p.move(move[0], move[1], self.board)
        shot = p.choose_shot(self.board)
        if shot:
            p.shoot(shot, self.board)
            self.check_deaths(p)
        self.board.clear_shots()
        return True

    def check_deaths(self, skip):
        '''
        Checks if any of the players are hit by a shot.
        Runs after any shot and kills any shot players.
        '''
        for p in self.pList:
            if p != skip:
                if p.is_shot(self.board):
                    self.lose(p)

    def win(self, p):
        ''' Gives winning conditions to player '''
        if isinstance(p.controller, Bot):
            pass
        print(f'{p.name} is the winner!')
        p.return_to_start()
        return p

    def lose(self, p):
        ''' Gives losing conditions to player '''
        if isinstance(p.controller, Bot):
            pass
        self.board.remove_player((p.x, p.y)) == 0
        self.pList.remove(p)
        p.return_to_start()
        print(f'{p.name} has lost.')
        return p

    def play_round(self):
        ''' Plays round returns player object if done and false otherwise '''
        for p in self.pList:
            self.player_turn(p)
            if (len(self.pList) == 1):
                return self.win(self.pList[0])
        self.roundCount += 1
        return False

    def play(self, roundNum):
        while (self.roundCount <= roundNum):
            result = self.play_round()
            if result:
                break
                return result
