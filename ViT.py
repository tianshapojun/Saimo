import torch
import torch.nn.functional as F
from einops import rearrange, repeat
from torch import nn
from torch.utils.data import Dataset,DataLoader
from tqdm import tqdm
import torchvision
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import os
import logging
#logging.basicConfig(level=logging.INFO)

MIN_NUM_PATCHES = 16
# https://blog.csdn.net/black_shuang/article/details/95384597

class TensorDataset(Dataset):
    # TensorData继承Dataset，重载了__init__, __getitem__,__lem__
    def __init__(self, data_tensor, target_tensor):
        # 实现将一组Tensor数据对封装成Tensor数据集
        self.data_tensor = data_tensor
        self.target_tensor = target_tensor

    def __getitem__(self, index):
        # 能够通过index得到数据集的数据
        return self.data_tensor[index], self.target_tensor[index]

    def __len__(self):
        # 能够通过len，得到数据集大小
        return self.data_tensor.size(0)  # size(0)返回当前张量维数的第一维

class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim, dropout=0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )
        self.norm = nn.LayerNorm(dim)

    def forward(self, x):
        return x + self.net(self.norm(x))


class Attention(nn.Module):
    def __init__(self, dim, heads=16, dim_head=64, dropout=0.):
        super().__init__()
        inner_dim = dim_head * heads  # dim_head x heads = 64 x 16
        self.heads = heads
        self.scale = dim ** -0.5

        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim),
            nn.Dropout(dropout)
        )
        self.norm = nn.LayerNorm(dim)

    def forward(self, x, mask=None):
        # x : b n (h d)
        # x shape: 1, 65, 1024
        b, n, _, h = *x.shape, self.heads
        qkv = self.to_qkv(self.norm(x)).chunk(3, dim=-1)  # dim=1024 -> innerdim x 3
        # q/k/v shape: 1, 65, 1024
        q, k, v = map(lambda t: rearrange(
            t, 'b n (h d) -> b h n d', h=h), qkv)  # inner dim = (heads x dim)
        # batch, inner dim, (heads x d) -> batch, heads, inner dim, dim
        # q/k/v.shape: 1, 16, 65, 64
        # 矩阵乘法
        dots = torch.einsum('bhid,bhjd->bhij', q, k) * \
            self.scale  # SCALE FUNCTION
        mask_value = -torch.finfo(dots.dtype).max  # mask

        if mask is not None:
            mask = F.pad(mask.flatten(1), (1, 0), value=True)
            assert mask.shape[-1] == dots.shape[-1], 'mask has incorrect dimensions'
            mask = mask[:, None, :] * mask[:, :, None]
            dots.masked_fill_(~mask, mask_value)
            del mask

        attn = dots.softmax(dim=-1)  # softmax

        # 将attention和value进行矩阵乘法施加注意力
        out = torch.einsum('bhij,bhjd->bhid', attn, v)
        # batch, heads, inner dim, dim
        out = rearrange(out, 'b h n d -> b n (h d)')
        out = self.to_out(out)  # inner dim->dim 的linear
        return x + out  # shape: 1, 65, 1024


class Transformer(nn.Module):
    def __init__(self, dim, depth, heads, dim_head, mlp_dim, dropout):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                Attention(dim, heads=heads,dim_head=dim_head, dropout=dropout),
                FeedForward(dim, mlp_dim, dropout=dropout)
            ]))

    def forward(self, x, mask=None):
        # x: 1, 65, 1024
        for attn, ff in self.layers:
            x = attn(x, mask=mask)
            x = ff(x)
        return x


class ViT(nn.Module):
    def __init__(self, *, image_size, patch_size, num_classes, dim, depth, heads, mlp_dim, channels=3, dim_head=64, dropout=0., emb_dropout=0.):
        super().__init__()
        assert image_size % patch_size == 0, 'Image dimensions must be divisible by the patch size.'
        num_patches = (image_size // patch_size) ** 2
        patch_dim = channels * patch_size ** 2
        assert num_patches > MIN_NUM_PATCHES, f'your number of patches ({num_patches}) is way too small for attention to be effective (at least 16). Try decreasing your patch size'

        self.patch_size = patch_size

        # 1, 65, dim=1024
        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        self.patch_to_embedding = nn.Linear(patch_dim, dim)
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim))
        self.dropout = nn.Dropout(emb_dropout)

        self.transformer = Transformer(
            dim, depth, heads, dim_head, mlp_dim, dropout)

        self.to_cls_token = nn.Identity()

        self.mlp_head = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, num_classes)
        )

    def forward(self, img, mask=None):
        # img 1, 3, 256, 256
        p = self.patch_size

        x = rearrange(
            img, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=p, p2=p)  # 1, 8*8, 32*32*3

        x = self.patch_to_embedding(x)  # linear 32*32*3->dim=1024
        b, n, _ = x.shape  # x: 1, 64, 1024

        # 1,1,dim->1,1,1024
        cls_tokens = repeat(self.cls_token, '() n d -> b n d', b=b)
        x = torch.cat((cls_tokens, x), dim=1)  # 1,(64+1),dim=1024
        # 1, 65, dim=1024 -> 1, 64, dim
        x += self.pos_embedding[:, :(n + 1)]  # 相加 TODO 这部分不理解
        x = self.dropout(x)  # 随机失活

        # x: 1, 65, 1024
        x = self.transformer(x, mask)

        x = self.to_cls_token(x[:, 0])
        return self.mlp_head(x)


if __name__ == "__main__":
    ddp = True
    dist.init_process_group(backend='nccl') 
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    model = ViT(
        image_size=32,
        patch_size=4,
        num_classes=10,
        dim=512,
        depth=3,
        heads=4,
        mlp_dim=1024,
        dropout=0,
        emb_dropout=0
    ).to(local_rank)
    model = DDP(model, device_ids=[local_rank], output_device=local_rank)
    logging.warning('DDP model initialization completed')
    """
    img = torch.randn(1024, 3, 256, 256)
    label = torch.randint(high=1000,size=(1024,))
    dataset = TensorDataset(img,label)
    dataloader = DataLoader(dataset,batch_size=16)
    """
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    my_trainset = torchvision.datasets.CIFAR10(root='./data', train=True, 
        download=True, transform=transform)
    if ddp == True:
        train_sampler = torch.utils.data.distributed.DistributedSampler(my_trainset)
        trainloader = torch.utils.data.DataLoader(my_trainset,batch_size=32, num_workers=2, sampler=train_sampler)
    else:
        trainloader = torch.utils.data.DataLoader(my_trainset,batch_size=32, num_workers=2)
    logging.warning('Data process completed')
    
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)
    loss_func = nn.CrossEntropyLoss().to(local_rank)
    
    model.train()
    iterator = tqdm(range(500))
    for epoch in iterator:
        trainloader.sampler.set_epoch(epoch)
        for data, label in trainloader:
            data, label = data.to(local_rank), label.to(local_rank)
            optimizer.zero_grad()
            prediction = model(data)
            loss = loss_func(prediction, label)
            loss.backward()
            iterator.desc = "loss = %0.3f" % loss
            optimizer.step()
    """
    optional mask, designating which patch to attend to
    mask = torch.ones(1, 8, 8).bool()
    preds = model(img, mask=mask)  # (1, 1000)
    print(preds.shape)
    """
