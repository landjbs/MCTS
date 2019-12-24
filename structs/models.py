import torch
import torch.nn as nn


class Conv(nn.Module):
    '''
    The Conv model is tasked with prediciting a vector (p) of move probabilities
    across the avaliable moves and a scalar (v) of win probability at the
    current state. To avoid shape issues, p always has length 8. Input board
    is a 4th order tensor with shape (boardSize, boardSize, 4) where the last
    order has indicies (0-shots, 1-walls, 2-enemies, 3-player).
    '''
    def __init_(self, lr, boardSize=25):
        super(Conv, self).__init__()
        # layers
        self.conv1 = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=1, stride=1, padding=0),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.dropout = nn.Dropout()
        self.lin1 = nn.Linear(7 * 7 * 64, 1000)
        self.lin2 = nn.Linear(1000, 10)
        # optimizers and loss
        self.optim = torch.optim.Adam(self.parameters(), lr=lr)
        self.criterion = nn.CrossEntropyLoss()

    # def calc_padding(self):

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(x)
        out = out.reshape(out.size(0), -1)
        out = self.dropout(out)
        out = self.lin1(out)
        out = self.lin2(out)
        return out

    def train_step(self, x, y):
        out = self(x)
        loss = self.criterion(out, y)
        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
        return loss
