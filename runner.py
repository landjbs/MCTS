from structs.models import Conv
from structs.player import Player
from structs.controller import Human, Dummy, Bot
from structs.game import Game
import torch
import numpy as np
import matplotlib.pyplot as plt

z = Conv(0.001)

bSize = 18
p1 = Player(1, 1, Bot('p1'))
p2 = Player(bSize, bSize, Bot('p2'))

for _ in range(1):
    x = Game([p1, p2], bSize, 0.3)
    print(x.board.board.shape)
    o = x.gen_train_tensor(p1)
    print(x.board.board.shape)
    # o = torch.tensor(np.zeros(shape=(1, 4, 20, 20)), dtype=torch.float)
    plt.imshow(o[0, :3, :, :].reshape(20, 20, 3))
    plt.show()
    plt.imshow(o[0, 3, :, :])
    plt.show()
    pY = torch.zeros(8)
    pY[1] = 1
    vY = 0
    z.train_step(o, pY, vY)
    # x.board.vis()
    # x.play(1000)
