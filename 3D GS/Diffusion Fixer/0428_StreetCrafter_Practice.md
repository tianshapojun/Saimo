# 基于StreetCrafter的实验报告
本次实验的目标：验证总结分析开源项目[**StreetCrafter**](https://github.com/zju3dv/street_crafter)的效果，指定后续工作计划

## 1. 训练配置
模型包含两个可训练的模块：Controllable Video Generation以及Crafting Dynamic 3D Scenes模块，前者为图像(视频)优化器后者为3DGS模型。

> 目前训练的是后者，对应的数据集为Waymo_val_49，主车自定义轨迹为向左横向平移3m；   
> 在训练过程中，在指定轮数添加diffusion模型生成的图像作为额外训练数据；   
> 可以通过1.图像优化器直接使用图像优化器生成高质图像；2.图像优化器作为gs模型的训练数据，由gs模型渲染图像；

下图为训练框架： 

<div align=center>
<img src="https://github.com/user-attachments/assets/2816c5e6-b2c4-495b-a3fe-780cf2b08da5" width="750px">
</div>

## 2. 结果分析
### 2.1 图像优化器

下图分别为GT、向左平移3m、向左平移6m、向左平移12m后的图像修复器生成的轨迹视频(100帧)。

https://github.com/user-attachments/assets/dc9d0235-70f9-47fc-bb6e-5af688a5ccf4

> 分析：   
> a. 产生视频基本满足要求，对于**大尺度平移泛化性较好，没有出现噪点伪影现象**；   
> b. 一致性问题依然存在，由于Video Generation产生的视频为25帧，所以在**短时间内保持时间一致性，该特性在长跨度内被破坏**；   
> c. **生成时间较长**，实验产生100帧图像需10-15分钟；   
> d. **细节存在误差**，下图为举例：标识生成效果较差；

<div align=center>
  <img src="https://github.com/user-attachments/assets/df581632-592e-4854-a4d9-0f97ca21f684" width="450px">
  <img src="https://github.com/user-attachments/assets/29da6096-fc37-436d-8db5-b5e3597e1a1b" width="450px">
</div>




