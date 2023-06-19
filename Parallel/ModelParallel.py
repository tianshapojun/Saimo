import argparse
from tqdm import tqdm
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import os

class ToyModel(nn.Module):
    def __init__(self):
        super(ToyModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Flatten(nn.Module):
    def forward(self, x):
        return x.view(-1, 16 * 5 * 5)

class ModelParallelToyModel(ToyModel):
    def __init__(self, *args, **kwargs):
        super(ModelParallelToyModel, self).__init__()

        self.seq1 = nn.Sequential(
            self.conv1,
            nn.ReLU(),
            self.pool,
            self.conv2,
            nn.ReLU(),
            self.pool,
            Flatten(),
            self.fc1
        ).to('cuda:0')

        self.seq2 = nn.Sequential(
            self.fc2,
            self.fc3
        ).to('cuda:1')

    def forward(self, x):
        #print(x.shape)
        x = self.seq2(self.seq1(x).to('cuda:1'))
        return x

def get_dataset():
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    my_trainset = torchvision.datasets.CIFAR10(root='./data', train=True, 
        download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(my_trainset, 
        batch_size=16, num_workers=2,shuffle=True)
    return trainloader

local_rank = 'cuda:0'

model_base = ToyModel()
model = ModelParallelToyModel(model_base)

trainloader = get_dataset()

# 要在构造DDP model之后，才能用model初始化optimizer。
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

loss_func = nn.CrossEntropyLoss().to('cuda:1')

model.train()
print('Train...')
iterator = tqdm(range(100))
for epoch in iterator:
    for data, label in trainloader:
        data, label = data.to(local_rank), label.to('cuda:1')
        optimizer.zero_grad()
        prediction = model(data)
        loss = loss_func(prediction, label)
        loss.backward()
        iterator.desc = "loss = %0.3f" % loss
        optimizer.step()
