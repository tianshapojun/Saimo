# 1. 总体方案

<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/779d131f-c76b-4c8b-890e-52ab9fae1c4f" width="750px">
</div>

# 2. 输入输出接口
## 2.1 流程图

<div align=center>
<img src="https://github.com/user-attachments/assets/4f8dc1a4-6d0f-4cde-990c-2478695e3b6e" width="750px">
</div>

> 输出文件为.txt形式，每一行(12个值,以空格间隔)记录某一帧某一物体信息，具体字段如下：

> 第1个值：代表帧数；    
> 第2个值：代表物体uid；   
> 第3个值：代表类别，可以为['Car', 'Van', 'Truck','Pedestrian', 'Person_sitting', 'Cyclist','Tram', 'Misc' , 'DontCare']；     
> 第4-7个值：代表物体的高宽长(hwl)(单位：米)；  
> 第8-10个值：代表3D bounding box的中心坐标(世界坐标系下)；  
> 第11个值：代表物体的航向角(-pi,pi]；  
> 第12个值：代表置信度；

## 2.2 预期结果可视化
视频中数据为KITTI_tracking数据集中train_00的1-150帧，用的是真值2D、3D标签，之后用感知算法的结果替换即可。

https://github.com/user-attachments/assets/58cc6fbf-8c9e-4473-9c4b-952965c54eb4

# 3. 实施计划
## 3.1 追踪模块计划

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/bc21ce88-85a4-4fab-b363-be15917299cf" width="750px">

# 4. demo

> 来自KITTI数据集，其中主车位姿信息由C2W给出；

https://github.com/user-attachments/assets/ba561b66-45f1-442a-a1a3-8f3f82e82bed

