# [Nuscenes](https://www.nuscenes.org/) 数据集标准化视角三维重建验证
*3.1*项目中，通过Nuscenes数据集验证标准化视角(->Waymo)的流程链路。

和之前的试验相比，主要的区别在于：
* 训练完整6路环视相机，而非3路前视相机，挑战性更大；
* 数据集频率更低，挑战性更大；

## 1. 数据集概述

| Sensor |  Information |
|:----------|:--------|
| 6x Camera   |12Hz capture frequency,1600 × 900 resolution|  
| 1x Lidar    |Spinning, 32 beams, 20Hz capture frequency, 360° horizontal FOV, −30° to 10° vertical FOV, ≤ 70m range, ±2cm accuracy, up to 1.4M points per second. |   
| 5x Radar    |≤ 250m range, 77GHz, FMCW, 13Hz capture frequency, ±0.1km/h vel. accuracy |  
| GPS & IMU   |GPS, IMU, AHRS. 0.2° heading, 0.1° roll/pitch,20mm RTK positioning, 1000Hz update rate |

对于关键帧(2Hz)，进行了数据标注，
> 如下图所示，Nuscenes数据集包含***6路环视相机***，相比Waymo数据集的***5路前/侧方相机***包含信息更全面，因此从Nuscenes->Waymo的参数转换可行性更高；   
> Nuscenes数据集采集的传感器关键帧频率为***2Hz***，低于Waymo数据的***10Hz***，相同时长的片段***包含信息量更少***；   
> Nuscenes数据集的后置摄像头包含了***部分主车主体***，影响***重建精度***；   
> Nuscenes Mini数据集一个片段约***20S***，即***40帧***数据；   
> Nuscenes Mini点云较Waymo更***稀疏***，例如前者40帧数据提取的背景点云数约***32万***，后者60帧数据提取的背景点云数约***106万***，***影响点云初始化以致训练的效果***；

---

<div align=center>
<img height="300" alt="image" src="https://github.com/user-attachments/assets/d08153ff-12ec-4b8c-addb-eed5114d9616" />
</div>


## 2. 训练细节

第一个阶段，将Nuscenes Mini数据集中的第一个场景进行训练，包含所有环视的6个相机。训练集和测试集的比例为4：1，总训练轮数为50000轮。
