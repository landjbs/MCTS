from structs.player import Player
from structs.controller import Human, Dummy, Bot
from structs.game import Game
import torch
import numpy as np
import matplotlib.pyplot as plt

bSize = 18
p1 = Player(1, 1, Bot('p1', 0.000001))
p2 = Player(bSize-1, bSize, Dummy('p2'))

# p2 = Player(bSize, bSize, Bot('p2'))

for i in range(1000):
    print(i)
    x = Game([p1, p2], bSize, 0)
    x.play(1000)
    # x.board.vis()
    # x.play(1000)

plt.plot(p1.controller.lVec)
plt.title(p1.name)
plt.show()

# plt.plot(p2.controller.lVec)
# plt.title(p2.name)
# plt.show()

for _ in range(10):
    print('hire')
    x = Game([p1, p2], bSize, 0.3)
    x.play(1000, vis=True)
