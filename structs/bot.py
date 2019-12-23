class Controller(object):
    def __init__(self, name):
        self.name = name

    def choose_move(self, moveList, board):
        pass

    def choose_shot(self, board):
        pass


class Human(Controller):
    ''' Human-controlled player for game api # TODO: finish '''
    def __init__(self, name):
        super(Human, self).__init__(name)

    def choose_move(self, moveList, board):
        pass

    def choose_shot(self, board):
        pass


class Dummy(Controller):
    ''' Dummy player that stays in one spot and never shoots '''
    def __init__(self, name):
        super(Dummy, self).__init__(name)

    def choose_move(self, moveList, board):
        return (0, 0)

    def choose_shot(self, board):
        return None


class Bot(Controller):
    ''' Bot-controlled player that learns across games '''
    def __init__(self, name):
        super(Bot, self).__init__(name)

    def choose_move(self, moveList, board):
        i = np.random.randint(0, len(moveList))
        return moveList[i]

    def choose_shot(self, board):
        i = np.random.randint(0, 5)
        return [0, 1, 2, 3, 4][i]