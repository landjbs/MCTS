from structs.models import Conv
from structs.player import Player
from structs.controller import Human, Dummy, Bot
from structs.game import Game
import torch

z = Conv(0.001)

bSize = 20
p1 = Player(1, 1, Bot('p1'))
p2 = Player(bSize, bSize, Bot('p2'))

for _ in range(1):
    x = Game([p1, p2], bSize, 0.3)
    o = x.gen_train_tensor(p1)
    pY = torch.zeros(8)
    pY[1] = 1
    vY = 0
    z.train_step(o, pY, vY)
    # x.board.vis()
    # x.play(1000)
