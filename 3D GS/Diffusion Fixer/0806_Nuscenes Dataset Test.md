# [Nuscenes](https://www.nuscenes.org/) 数据集标准化视角三维重建验证
*3.1*项目中，通过Nuscenes数据集验证标准化视角(->Waymo)的流程链路。

## 1. 数据集概述
<div align=center>
<img height="300" alt="image" src="https://github.com/user-attachments/assets/d08153ff-12ec-4b8c-addb-eed5114d9616" />
</div>

---

> 如上图所示，Nuscenes数据集包含***6路环视相机***，相比Waymo数据集的***5路前/侧方相机***包含信息更全面，因此从Nuscenes->Waymo的参数转换可行性更高；   
> Nuscenes数据集采集的传感器频率为***2Hz***，低于Waymo数据的***10Hz***，相同时长的片段包含信息量更少；   
> Nuscenes数据集的后置摄像头包含了***部分主车主体***，影响重建精度；   
> Nuscenes Mini数据集一个片段约***20S***，即***40帧***数据；   
> Nuscenes Mini点云较Waymo更***稀疏***，例如前者40帧数据提取的背景点云数约***32万***，后者60帧数据提取的背景点云数约***106万***；

## 2. 训练细节

第一个阶段，将Nuscenes Mini数据集中的第一个场景进行训练，包含所有环视的6个相机。训练集和测试集的比例为4：1，总训练轮数为50000轮。

