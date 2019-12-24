import torch
import torch.nn as nn


class Conv(nn.Module):
    def __init_(self, lr):
        super(Conv, self).__init__()
        # layers
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=5, stride=1, padding=2),
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
