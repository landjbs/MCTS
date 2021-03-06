import numpy as np
from structs.models.conv import Conv
from structs.models.tree import Node, Search


class Controller(object):
    def __init__(self, name):
        self.name = name

    def choose_move(self, player):
        pass

    def choose_shot(self, board):
        pass


class Human(Controller):
    ''' Human-controlled player for game api # TODO: finish '''
    def __init__(self, name):
        super(Human, self).__init__(name)

    def choose_move(self, player):
        pass

    def choose_shot(self, board):
        pass


class Dummy(Controller):
    ''' Dummy player that stays in one spot and never shoots '''
    def __init__(self, name):
        super(Dummy, self).__init__(name)

    def choose_move(self, player):
        return (0, 0)

    def choose_shot(self, board):
        return None


class Bot(Controller):
    ''' Bot-controlled player that learns across games '''
    def __init__(self, name, lr):
        super(Bot, self).__init__(name)
        self.nn = Conv(lr)
        self.lVec = []

    def conv_choose_move(self, validMoves, board):
        # i = np.random.randint(0, len(moveList))
        # return moveList[i]
        moveGuess = np.random.randint(0, len(validMoves))
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                 (1, 0), (-1, 1), (0, 1), (1, 1)]
        if (1, 1) in validMoves:
            pY = moves.index((1, 1))
        elif (-1, -1) in validMoves:
            pY = moves.index((-1, -1))
        elif (0, 1) in validMoves:
            pY = moves.index((0, 1))
        elif (1, 0) in validMoves:
            pY = moves.index((1, 0))
        else:
            pY = moves.index(validMoves[np.random.randint(0, len(validMoves))])
        p, v = self.nn.forward(board)
        pMax = p.topk(1)[1].item()
        # if moves[pMax] in validMoves:
        #     pY = pMax
        #     print(moves[pMax])
        # else:
        #     pY = moveGuess
        l = self.nn.eval_and_prop(p, v, pY, 1)
        self.lVec.append(l)
        move = moves[pMax]
        # print(move)
        return move

    def choose_move(self, player):
        # root = Node(state=player, )
        pass

    def choose_shot(self, board):
        # i = np.random.randint(0, 5)
        # return [0, 1, 2, 3, 4][i]
        return 0
