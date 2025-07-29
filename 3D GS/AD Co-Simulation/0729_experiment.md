# 0729 AD联仿感知模块评估

# 1. 实验设置和结果
实验中三维重建模块与[UniAD](https://arxiv.org/abs/2212.10156)联仿，评估其感知模块并与YOLO10进行比较，相关的实验设置和结果如下图所示。

<div align=center>
<img src="https://github.com/user-attachments/assets/985536a2-8342-4acb-b3aa-a38e1ad2f281" width="1000px">
</div>


# 2. 相关视频
## 2.1 Waymo_121 

GT值和YOLO感知结果汇总如下：

https://github.com/user-attachments/assets/d85c1ee7-2eed-4133-8d42-55bd64d3530d

其中YOLO行框上的数字代表***置信度***；Matched行框上的数字代表***IoU***，绿色框表示匹配上的GT框，红色框表示未匹配上的GT框；



