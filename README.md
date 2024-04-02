# Linux之显示文件或目录所占用的磁盘空间
du -sh ./* 显示当前目录下所有文件的大小

-s 显示文件或整个目录的大小，默认单位为KB

-h输出文件系统分区使用情况，例如：1KB、1MB、1GB

# Pytorch各版本

https://pytorch.org/get-started/previous-versions/

# conda取消自动进入base环境
取消进base: conda config --set auto_activate_base false

重新进base: conda config --set auto_activate_base true

# Anaconda删除虚拟环境
方法一：

第一步：首先退出环境
conda deactivate
 
第二步：查看虚拟环境列表，此时出现列表的同时还会显示其所在路径
conda env list
 
第三步：删除环境
conda env remove -p 要删除的虚拟环境路径

conda env remove -p /home/kuucoss/anaconda3/envs/tfpy36   #我的例子

方法二：

第一步：首先退出环境
conda deactivate
 
第二步：删除环境
conda remove -n  需要删除的环境名 --all

# Anaconda 复制环境
#环境复制命令：
conda create -n traget_env_name --clone source_env_name

举例：
conda create -n my_numpy --clone numpy 
(创建一个新的环境my_numpy，由numpy复制而来)

# Anaconda镜像源
1.添加镜像channel。

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

2.删除镜像channel。

conda config --remove channels  https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

3.展示目前已有的镜像channel。

conda config --show channels

https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/

https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/

https://mirrors.aliyun.com/pypi/simple/

https://pypi.douban.com/simple

https://pypi.mirrors.ustc.edu.cn/simple/

# 在服务器上git clone github项目的过程

https://blog.csdn.net/a61022706/article/details/122228080

# 服务器运行Tensorboard本地查看的方法
服务器终端中输入

$ tensorboard --logdir=./runs

本地终端中输入：

ssh -L 16006:127.0.0.1:6006 user@sevcerip 

16006:本地端口号;\
127.0.0.1:本地ip;\
6006:服务器端口号;

浏览器输入

http://127.0.0.1:16006/

# Python 添加并存储logger

logger = logging.getLogger(\_\_name\_\_) \
logger.setLevel(level = logging.INFO) \
current_date = datetime.now().strftime('%Y%m%d%H%M%S') \
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') \
handler = logging.FileHandler("/content/gdrive/MyDrive/Models/STFGNN/"+str(current_date)+"_log.txt") \
handler.setLevel(logging.INFO) \
handler.setFormatter(formatter) \
sh = logging.StreamHandler() \
sh.setLevel(logging.INFO) \
sh.setFormatter(formatter) \
logger.addHandler(handler) \
logger.addHandler(sh)

# Python pip 错误：OSError: Could not find a suitable TLS CA certificate bundle, invalid path: /etc/ssl/certs/ca-certificates.crt

sudo update-ca-certificates

# Python Pytorch Torchvision
https://pytorch.org/get-started/locally/

| `torch`            | `torchvision`      | Python              |
| ------------------ | ------------------ | ------------------- |
| `main` / `nightly` | `main` / `nightly` | `>=3.8`, `<=3.11`   |
| `2.0`              | `0.15`             | `>=3.8`, `<=3.11`   |
| `1.13`             | `0.14`             | `>=3.7.2`, `<=3.10` |
| `1.12`             | `0.13`             | `>=3.7`, `<=3.10`   |
| `1.11`  | `0.12`            | `>=3.7`, `<=3.10`         |
| `1.10`  | `0.11`            | `>=3.6`, `<=3.9`          |
| `1.9`   | `0.10`            | `>=3.6`, `<=3.9`          |
| `1.8`   | `0.9`             | `>=3.6`, `<=3.9`          |
| `1.7`   | `0.8`             | `>=3.6`, `<=3.9`          |
| `1.6`   | `0.7`             | `>=3.6`, `<=3.8`          |
| `1.5`   | `0.6`             | `>=3.5`, `<=3.8`          |
| `1.4`   | `0.5`             | `==2.7`, `>=3.5`, `<=3.8` |
| `1.3`   | `0.4.2` / `0.4.3` | `==2.7`, `>=3.5`, `<=3.7` |
| `1.2`   | `0.4.1`           | `==2.7`, `>=3.5`, `<=3.7` |
| `1.1`   | `0.3`             | `==2.7`, `>=3.5`, `<=3.7` |
| `<=1.0` | `0.2`             | `==2.7`, `>=3.5`, `<=3.7` |

# vscode 快捷方式

- ALT+ 鼠标左键 选中多行同时编辑； 
- 选中多行,按TAB键可统一向右移动； 
- 按住 CTRL + ALT，再按键盘上的上或下键，可以使一列上出现多个光标；
- 选中一段文字，按SHIFIT + ALT + i，在每行末尾都会出现光标； 
- 按SHIFIT + ALT，再使用鼠标拖动，也可以出现竖直的列光标，同时可以选中多列；
- 选中文本后，CTRL + [ 和 CTRL + ] 可实现文本的向左移动 和 向右移动； 
- CTRL + SHIFIT + L 选中编辑代码中相同的内容； 

# Cannot access waymo_open_dataset_motion_v_1_1_0

Could you try registering (or re-registering) at https://waymo.com/open/licensing/ This process should grant you access to the dataset files.

# Torch Tricks
## Calculate the number of parameters 
total = sum([param.nelement() for param in model.parameters()])

print("Number of parameter: %.2fM" % (total/1e6))

## pip install mayavi fails building wheel
from https://github.com/enthought/mayavi/issues/1232
pip install https://github.com/enthought/mayavi/zipball/master

## 特定GPU可见
1.CUDA_VISIBLE_DEVICES='1' python train.py

2.in .py file

import os

os.environ['CUDA_VISIBLE_DEVICES'] = '1,2,3'(在import torch 之前)

