# Linux之显示文件或目录所占用的磁盘空间
`du -sh ./*` 显示当前目录下所有文件的大小

-s 显示文件或整个目录的大小，默认单位为KB

-h输出文件系统分区使用情况，例如：1KB、1MB、1GB

# 查看Linux版本
`lsb_release -a`

# 查找指定进程号
例如：0522.py结尾的python文件

`ps -ef | grep 0522.py`

# Pytorch各版本

https://pytorch.org/get-started/previous-versions/

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

# Anaconda
## conda取消自动进入base环境
取消进base: `conda config --set auto_activate_base false`

重新进base: `conda config --set auto_activate_base true`

## Anaconda删除虚拟环境
方法一：

第一步：首先退出环境
`conda deactivate`
 
第二步：查看虚拟环境列表，此时出现列表的同时还会显示其所在路径
`conda env list`
 
第三步：删除环境
`conda env remove -p 要删除的虚拟环境路径`

`conda env remove -p /home/kuucoss/anaconda3/envs/tfpy36`   #我的例子

方法二：

第一步：首先退出环境
`conda deactivate`
 
第二步：删除环境
`conda remove -n  需要删除的环境名 --all`

## Anaconda 复制环境
#环境复制命令：
`conda create -n traget_env_name --clone source_env_name`

举例：
`conda create -n my_numpy --clone numpy`
(创建一个新的环境my_numpy，由numpy复制而来)

## Anaconda镜像源
1.添加镜像channel。

`conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`

2.删除镜像channel。

`conda config --remove channels  https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`

3.展示目前已有的镜像channel。

`conda config --show channels`

https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/

https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/linux-64/

https://mirrors.aliyun.com/pypi/simple/

https://pypi.douban.com/simple

https://pypi.mirrors.ustc.edu.cn/simple/

## conda pack迁移环境

https://blog.csdn.net/qq_44722189/article/details/140957031

> pip install conda-pack   
> conda pack -n your_env_name -o your_env_name.tar.gz   
> tar -xzvf your_env_name.tar.gz -C conda3/envs/your_env   

# 在服务器上git clone github项目的过程

https://blog.csdn.net/a61022706/article/details/122228080

# 服务器运行Tensorboard本地查看的方法
服务器终端中输入

`$ tensorboard --logdir=./runs`

本地终端中输入：

`ssh -L 16006:127.0.0.1:6006 user@sevcerip `

16006:本地端口号;\
127.0.0.1:本地ip;\
6006:服务器端口号;

浏览器输入

http://127.0.0.1:16006/

# Python 添加并存储logger

```python
logger = logging.getLogger(__name__) 
logger.setLevel(level = logging.INFO) 
current_date = datetime.now().strftime('%Y%m%d%H%M%S') 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
handler = logging.FileHandler("/content/gdrive/MyDrive/Models/STFGNN/"+str(current_date)+"_log.txt") 
handler.setLevel(logging.INFO) 
handler.setFormatter(formatter) 
sh = logging.StreamHandler() 
sh.setLevel(logging.INFO) 
sh.setFormatter(formatter) 
logger.addHandler(handler) 
logger.addHandler(sh)
```

# Python pip 错误：OSError: Could not find a suitable TLS CA certificate bundle, invalid path: /etc/ssl/certs/ca-certificates.crt

`sudo update-ca-certificates`

# ffmpeg 用例
`ffmpeg -framerate 10 -i ./output/1014_sim_7/%05d.png -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -r 10 -pix_fmt yuv420p ./output/10014_sim_7.mp4`

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
```python
total = sum([param.nelement() for param in model.parameters()])

print("Number of parameter: %.2fM" % (total/1e6))
```
## pip install mayavi fails building wheel
from https://github.com/enthought/mayavi/issues/1232

pip install https://github.com/enthought/mayavi/zipball/master

## 特定GPU可见
1. `CUDA_VISIBLE_DEVICES='1' python train.py`

2. in .py file
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1,2,3'(在import torch 之前)
```

## 固定随机数种子
https://ispacesoft.com/71697.html

更新torch库中一些不确定性内容以及相应固定方法    
https://pytorch.org/docs/stable/notes/randomness.html

```python
def seed_torch(seed=1029):

	random.seed(seed)
 
	os.environ['PYTHONHASHSEED'] = str(seed) # 为了禁止hash随机化，使得实验可复现
 
	np.random.seed(seed)
 
	torch.manual_seed(seed)
 
	torch.cuda.manual_seed(seed)
 
	torch.cuda.manual_seed_all(seed) # if you are using multi-GPU.
 
	torch.backends.cudnn.benchmark = False
 
	torch.backends.cudnn.deterministic = True

	os.environ['CUBLAS_WORKSPACE_CONFIG']=':16:8'
 	torch.use_deterministic_algorithms(True)

seed_torch()
```

## pytorch 显存分配及模型推理时间统计

显存分配：https://zhuanlan.zhihu.com/p/527143823?utm_id=0

推理速度计算：https://zhuanlan.zhihu.com/p/376925457

# Colab 使用技巧
## 文件批量打包下载
```python
!zip -r /content/output.zip /content/ml-depth-pro/output
from google.colab import files
files.download("/content/output.zip")
```

# CV 
## 深度/距离转颜色
```python
colors = cv2.applyColorMap(cv2.convertScaleAbs(dist, alpha=1), cv2.COLORMAP_JET)
pcd.colors = o3d.utility.Vector3dVector(colors[:,0,:].clip(0, 255)/255)
```
