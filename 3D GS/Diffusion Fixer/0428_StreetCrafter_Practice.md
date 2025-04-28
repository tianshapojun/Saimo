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
