# Nuscenes数据集12摄像头原型验证

功能：验证从n个摄像头到m(m >> n)个摄像头的流程链路。对于Nuscenes数据集，即从6路相机推广到12路相机。

过程中的问题点包括：
* n路相机的安装位置，可根据原始相机位置旋转一定角度获取，详情见[自定义相机推导流程记录](https://github.com/tianshapojun/Saimo/blob/main/3D%20GS/0801_Customized%20Cameras.md)；
* 训练参数调优；

## 1. 方案设计
<div align=center> Fig.1 方案设计
  <img width="900ptx" alt="image" src="https://github.com/user-attachments/assets/bab0fa35-5c23-44f9-a2df-85b30b9bb46e" />   
</div>
