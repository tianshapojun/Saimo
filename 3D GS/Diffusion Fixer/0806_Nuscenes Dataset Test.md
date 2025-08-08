# [Nuscenes](https://www.nuscenes.org/) 数据集标准化视角三维重建验证
3.1项目中，子课题包括通过Nuscenes数据集验证标准化视角(->Waymo)的流程链路。

和之前的试验相比，主要的区别在于：
* 训练完整6路环视相机，而非3路前视相机，挑战性更大；
* 数据集频率更低，点云数量更少，挑战性更大；

## 1. 数据集概述

| Sensor |  Information |
|:----------|:--------|
| 6x Camera   |12Hz capture frequency,1600 × 900 resolution|  
| 1x Lidar    |Spinning, 32 beams, 20Hz capture frequency, 360° horizontal FOV, −30° to 10° vertical FOV, ≤ 70m range, ±2cm accuracy, up to 1.4M points per second. |   
| 5x Radar    |≤ 250m range, 77GHz, FMCW, 13Hz capture frequency, ±0.1km/h vel. accuracy |  
| GPS & IMU   |GPS, IMU, AHRS. 0.2° heading, 0.1° roll/pitch,20mm RTK positioning, 1000Hz update rate |

安装位置如下图所示，对于关键帧(2Hz)进行了数据标注，
> Nuscenes数据集包含***6路环视相机***，相比Waymo数据集的***5路前/侧方相机***包含信息更全面，因此从Nuscenes->Waymo的参数转换可行性更高；   
> Nuscenes数据集采集的传感器关键帧频率为***2Hz***，低于Waymo数据的***10Hz***，相同时长的片段***包含信息量更少***；   
> Nuscenes数据集的后置摄像头包含了***部分主车主体***，影响***重建精度***；   
> Nuscenes Mini数据集一个片段约***20S***，即***40帧***数据；   
> Nuscenes Mini点云较Waymo更***稀疏*** (Waymo激光雷达的vFOV：top-[-17.6°,2.4°]; F,SL,SR,R-[-90°,30°])，例如前者40帧数据提取的背景点云数约***32万***，后者60帧数据提取的背景点云数约***106万***，***影响点云初始化以致训练的效果***；

---

<div align=center>
<img height="220" alt="image" src="https://github.com/user-attachments/assets/d08153ff-12ec-4b8c-addb-eed5114d9616" />
<img height="220" alt="image" src="https://github.com/user-attachments/assets/2385733a-6355-4700-bd22-09a7e84fd30f" />
</div>

作为比较，Waymo采集车各传感器的安装位置如下：

<div align=center>
<img height="400" alt="image" src="https://github.com/user-attachments/assets/f1e339b5-9556-4ed1-937f-a67ee066a306" />
</div>

## 2. 训练细节
### 2.1 第一阶段
在第一个阶段，我们训练Nuscenes Mini数据集中的场景。训练集和测试集的比例为4：1，总训练轮数为50000轮。

> [0906] 对于片段01，训练集PSNR：24.82，测试集PSNR：20.71，不符合预期；   
> **原因分析**：数据质量较低，且还原难度较高，环境复杂(有停车场、有路口、有玻璃建筑等)且初始点云稀疏；

针对不同场景，具体试验结果如下：

| Experiment   |   DataSet |   Camera | Batch  |    Train_PSNR(↑) |   Test_PSNR(↑) | Batch  |    Train_PSNR(↑) |   Test_PSNR(↑) |
|:----------|----------:|------:|--------:|--------:|--------:|--------:|--------:|--------:|
| Exp0   |   mini_001 |0-5    |7000 |    19.94|    19.15|50000 |    24.82|    20.71|
| Exp1   |   mini_001 |0-2    |7000 |    22.90|    19.48|30000 |    28.14|    20.65|
| Exp2   |   mini_005 |0-5    |7000 |    19.67|    15.15|60000 |    25.93|     15.58|
| Exp3   |   mini_005 |0-2    |7000 |    20.09|    14.69|30000 |    28.37|     14.84| 
| Exp4   |   mini_005 |0-4    |7000 |    18.63|    14.78|90000 |    27.60|     14.49|
