# 1. 总体方案 (Version 0.1)
本次方案主要的修改点包含2个方面，
> 1. 单目感知模型除了端到端的车辆检测外，增加基于2D bbx+深度预估的人、障碍物检测，具体见 [Mono Detection Using 2D bbx + Depth Map](https://github.com/tianshapojun/Saimo/blob/main/Monocular%20Camera%20Detection/Mono%20Detection%20Using%202D%20bbx%20%2B%20Depth%20Map.md)；
> 2. 优化追踪结果的后处理模块，增加动、静物体判别以及轨迹优化，具体见 [Pb1_Shift in Location and Yaw](https://github.com/tianshapojun/Saimo/blob/main/Monocular%20Camera%20Detection/Pb1_Shift%20in%20Location%20and%20Yaw.md)；

<div align=center>
<img src="https://github.com/user-attachments/assets/7800042b-ae4a-4026-986d-da604516f6a9" width="700px">
</div>
