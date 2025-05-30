# 1. 问题描述
以KITTI为例的3D感知开源数据集的打标类别一般为车、人，对于相关需求：障碍物(锥桶)已至后续可能的交通灯等其它目标物没有相应数据，因此调研相关技术路线以达成其它类别目标物3D感知的目标。

# 2. 文献调研
相关结果通过思维导图的方式如下： 

<div align=center>
<img src="https://github.com/user-attachments/assets/8bd20bb1-58a6-4d61-b2aa-8f2b38cf9473">
</div>



# 3. 方案概述
由于2D单目感知的高精度，深度预估通用模型的发展，以及部分类别物体数据的缺失，选用了2D+深度的单目感知方案。目前该方案适用于人、障碍物(锥桶)标签。

对于已知像素坐标 $u,v$以及深度 $z$，通过下述公式获得坐标 $x,y$，

$$
x = \frac{u-u_0}{f} \cdot z,
$$

$$ 
y = \frac{v-v_0}{f} \cdot z.
$$ 

目前存在待优化的点包括：
> 1. 物体的中心点如何确定：最简单的方位是用2D包围盒的中心确认为物体中心，但存在的问题包括：a. 物体被遮挡；b. 行人2D框中心处于背景位置。目前的解决方法是以分位数的深度替代，主要针对第二个问题。
> 2. 物体的航向角如何确定：对于障碍物(锥桶)航向角不重要，对于动态的人可以通过追踪得到的轨迹辅助推断航向角，但对于静止的行人无法给出更精准的结果。目前统一以0度作为初始化。

## 3.1 2D检测框算法 
基于[YOLO10](https://github.com/THU-MIG/yolov10)模型，
> 标签：人，开源训练好的权重包含该部分内容；    
> 标签：锥桶，通过图片(约1900张)进行云端训练；

## 3.2 深度图获取算法
基于[Depth Pro](https://github.com/apple/ml-depth-pro)，获得图像的绝对深度(metric depth)；示例如下：

<div align=center>
<img src="https://github.com/user-attachments/assets/10042ecc-0446-4d16-b07e-3830fc6fa6a1" width="500px">
</div>

# 4. demo

https://github.com/user-attachments/assets/3d52cff5-2198-4690-bb73-5a94151b16df

