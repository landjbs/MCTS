import torch
import torch.nn as nn


class Conv(nn.Module):
    '''
    The Conv model is tasked with prediciting a vector (p) of move probabilities
    across the avaliable moves and a scalar (v) of win probability at the
    current state. To avoid shape issues, p always has length 8. Input board
    is a 4th order tensor with shape (boardSize, boardSize, 4) where the last
    order has indicies (0-shots, 1-walls, 2-enemies, 3-player).
    Sizes are currently hard-coded.
    '''
    def __init__(self, lr, boardSize=20):
        super(Conv, self).__init__()
        # layers
        self.conv1 = nn.Sequential(
            nn.Conv2d(4, 20, kernel_size=1, stride=1, padding=0),
            nn.ReLU()
            ) #nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Sequential(
            nn.Conv2d(20, 20, kernel_size=1, stride=1, padding=0),
            nn.ReLU()
            ) #nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout = nn.Dropout(p=0.3)
        self.lin1 = nn.Linear(3 * 3 * 20, 1000)
        self.pLin = nn.Linear(1000, 8)
        self.soft = nn.Softmax(dim=1)
        self.vLin = nn.Linear(1000, 1)
        self.sig = nn.Sigmoid()
        # optimizers and loss
        self.optim = torch.optim.Adam(self.parameters(), lr=lr)
        # self.pCriterion = nn.CrossEntropyLoss()
        self.vCriterion = nn.BCELoss()

    def pCriterion(self, p, target):
        pC = p[0, target]
        pLog = torch.log(pC)
        loss = -(pLog)
        return loss

    def forward(self, boardTensor):
        convOut = self.conv1(boardTensor)
        convOut = self.conv2(convOut)
        convOut = convOut.reshape(convOut.size(0), -1)
        convOut = self.dropout(convOut)
        linOut = self.lin1(convOut)
        p = self.soft(self.pLin(linOut))
        v = self.sig(self.vLin(linOut))[0]
        # print(f'p: {p} | v: {v}')
        return p, v

    def eval_and_prop(self, pX, vX, pY, vY):
        pLoss = self.pCriterion(pX, pY)
        vLoss = self.vCriterion(vX, torch.tensor([vY], dtype=torch.float))
        loss = pLoss + vLoss
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
        return loss

    def train_step(self, x, yP, yV):
        p, v = self(x)
        return self.eval_and_prop(p, v, yP, yV)
