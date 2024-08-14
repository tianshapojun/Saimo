# 1. 总体方案

<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/779d131f-c76b-4c8b-890e-52ab9fae1c4f" width="750px">
</div>
    
> 关于追踪算法细节，详见[[EagerMOT相关细节](https://www.overleaf.com/read/cvwndfjdztgk#36a457)]


# 2. 输入输出接口
> **追踪+C2W模块输入**：为图像文件夹路径，标签文件夹路径，外参文件夹路径；

> 图像文件夹    
> 其中图片按时间顺序从小到大命名，例如'001.png'，'002.png'，'003.png'...

> 标签文件夹    
> 其中标签文件按图像命名规则一一对应，例如'001.txt'，'002.txt'，'003.txt'...     
> 标签文件按照kitti格式，共16个值，    
> 第1个值：代表类别，    
> 第2个值：代表物体是否被截断,固定为-1，    
> 第3个值：代表物体是否被遮挡,固定为-1，    
> 第4个值：代表物体的观察角度,固定为0，   
> 第5-8个值：代表物体的2D bounding box,分别为xmin、ymin、xmax、ymax，    
> 第9-11个值：代表物体的高宽长(hwl)(单位：米)，    
> 第12-14个值：代表3D bounding box的中心坐标(相机坐标系下)，    
> 第15个值：代表物体的航向角，    
> 第16个值：代表置信度，
 
> 外参文件夹支持3种格式，    
> 1.提供C2W信息，其中外参文件按图像命名规则一一对应，例如'001.txt'，'002.txt'，'003.txt'...     
> C2W为1行16列，即4x4矩阵变形，以空格间隔，表示相机坐标系和世界坐标系之间的转换，    
> 2.提供pose信息，'pose.txt'；C2V信息，'c2v.txt'    
> pose为n行6列，其中n与图片数量一致，每一行的数值分别代表    
> lat：latitude of the oxts-unit (deg)  #维度    
> lon：longitude of the oxts-unit (deg) # 经度    
> alt：altitude of the oxts-unit (m) # 高度    
> roll：roll angle (rad)，        
> pitch：pitch angle (rad)，    
> yaw：heading (rad)，    
> C2V为1行16列，即4x4矩阵变形，以空格间隔，表示相机坐标系和车辆(GPS)坐标系之间的转换，    
> 3.提供x/y/yaw信息，'xyyaw.txt'；C2V信息，'c2v.txt'    
> pose为n行3列，其中n与图片数量一致，每一行的数值分别代表    
> x：世界坐标系下    
> y：世界坐标系下    
> yaw：航向角    
> C2V为1行16列，即4x4矩阵变形，以空格间隔，表示相机坐标系和车辆(GPS)坐标系之间的转换，   

> **总体输出文件**为.txt形式，每一行(12个值,以空格间隔)记录某一帧某一物体信息，具体字段如下：

> 第1个值：代表帧数；    
> 第2个值：代表物体uid；   
> 第3个值：代表类别，可以为['Car', 'Van', 'Truck','Pedestrian', 'Person_sitting', 'Cyclist','Tram', 'Misc' , 'DontCare']；     
> 第4-7个值：代表物体的高宽长(hwl)(单位：米)；  
> 第8-10个值：代表3D bounding box的中心坐标(世界坐标系下)；  
> 第11个值：代表物体的航向角(-pi,pi]；  
> 第12个值：代表置信度；
## 2.1 流程图

<div align=center>
<img src="https://github.com/user-attachments/assets/4f8dc1a4-6d0f-4cde-990c-2478695e3b6e" width="750px">
</div>

## 2.2 预期结果可视化
视频中数据为KITTI_tracking数据集中train_00的1-150帧，用的是真值2D、3D标签，之后用感知算法的结果替换即可。

https://github.com/user-attachments/assets/58cc6fbf-8c9e-4473-9c4b-952965c54eb4

# 3. 实施计划
## 3.1 追踪模块计划

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/bc21ce88-85a4-4fab-b363-be15917299cf" width="750px">

# 4. demo

> 来自KITTI数据集，其中主车位姿信息由C2W给出；

https://github.com/user-attachments/assets/ba561b66-45f1-442a-a1a3-8f3f82e82bed

https://github.com/user-attachments/assets/25fc1ade-92ce-45a8-8b2c-c66a94eaf330


