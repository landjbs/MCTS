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

for _ in range(1000):
    x = Game([p1, p2], bSize, 0.3)
    x.play(1000)
    # x.board.vis()
    # x.play(1000)


x.play(1000, vis=True)
