# Pytorch各版本

https://pytorch.org/get-started/previous-versions/

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
