# Nuscenes数据集12摄像头原型验证

功能：验证从n个摄像头到m(m >> n)个摄像头的流程链路。对于Nuscenes数据集，即从6路相机推广到12路相机。

过程中的问题点包括：
* n路相机的安装位置，可根据原始相机位置旋转一定角度获取，详情见[自定义相机推导流程记录](https://github.com/tianshapojun/Saimo/blob/main/3D%20GS/0801_Customized%20Cameras.md)；
* 训练参数调优；

## 1. 方案设计
<div align=center> 
  <img width="600ptx" alt="image" src="https://github.com/user-attachments/assets/bab0fa35-5c23-44f9-a2df-85b30b9bb46e" />   
</div>
<div align=center> 
  Fig.1 方案设计
</div>

---

由于Nuscenes数据集传感器数据无法做到帧精确匹配+点云稀疏+标注质量不高，因此采用仿射变换的修复模式。

对于训练参数调优，包含：

| Name                   |      Detail             | 
|:-----------------------|:------------------------|
|lambda_l1               |重建L1损失权重            | 
|lambda_novel            |修复图像损失权重          |
|lambda_novel_l1         |修复图像重建L1损失权重     |
|densification_interval  |高斯点稠密化周期          |
|opacity_reset_interval  |不透明度重置周期          |
|lambda_depth_lidar      |雷达深度损失权重          |
|densify_grad_threshold  |稠密化梯度阈值            |

