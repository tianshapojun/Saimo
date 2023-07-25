# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
"""
Backbone modules.
"""
from collections import OrderedDict

import torch
import torch.nn.functional as F
import torchvision
from torch import nn
from torchvision.models._utils import IntermediateLayerGetter
from typing import Dict, List
import torch.distributed as dist
from typing import Optional
from torch import Tensor

class BackboneBase(nn.Module):

    def __init__(self, backbone: nn.Module, train_backbone: bool, num_channels: int, return_interm_layers: bool):
        super().__init__()
        for name, parameter in backbone.named_parameters():
            if not train_backbone or 'layer2' not in name and 'layer3' not in name and 'layer4' not in name:
                parameter.requires_grad_(False)
        if return_interm_layers:
            return_layers = {"layer1": "0", "layer2": "1", "layer3": "2", "layer4": "3"}
        else:
            return_layers = {'layer4': "0"}
        self.body = IntermediateLayerGetter(backbone, return_layers=return_layers)
        self.num_channels = num_channels
        #self.lin1  = nn.Linear(7,14)

    def forward(self, x):
        xs = self.body(x)['0']
        #xs = self.lin1(xs)
        return xs



if __name__=='__main__':
    train_backbone = 0
    return_interm_layers = 0
    backbone =  torchvision.models.resnet18(pretrained=True)
    Backbone = BackboneBase(backbone,train_backbone,num_channels = 512,return_interm_layers = 0)
    out = Backbone(torch.rand(3, 3, 224, 224))
    print(out.shape)
    #for name,para in Backbone.named_parameters():
        #print(name,para.requires_grad)
