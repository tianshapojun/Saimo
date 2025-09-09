# 修复器点云图优化及传感参数更改

功能：由于支持根据Simpro车模尺寸安装相机传感器并渲染的需求，根据现有重建模型框架我们需要一个较好的修复器修复效果来支持训练。

## 1. 方案设计
点云图是修复器输入最重要的组成部分。原始相机参数下的点云图如Fig.1所示。

观察到的主要现象是：黑色(即无染色)部分占比较多(除天空和远处/高处的物体外，还包括近处的地面)；原因是雷达安装较高并且由于FOV问题车辆附近的地面无法扫到，以致于无法渲染
(相机在n-m到n-1帧之间能够扫到n帧主车周围的点，但无法完全能覆盖，所以出现部分点有染色的情况)。

解决思路有2种：
* 重新训练修复器，使得其泛化性更强，使用当前情况；
* 优化输入数据，使其分布与训练数据尽可能一致。

考虑到时间周期，采用第二种方案。

### 1.1 俯仰角调整
调整俯仰角的主要目的是为了控制相机渲染的最近距离。
假设相机光心和相平面底边连线发出的射线和地面的夹角为 $$\alpha$$，相机离地面的高度为 $$d$$，那么渲染的最近距离为 $$\frac{d}{tan(\alpha)}$$。

### 1.2 内参/分辨率改变
分辨率改变的主要目的和俯仰角调整的目的相同。

内参改变的主要目的是使同一个物体在像素平面上的图像更聚集(看上去更"小")。

对于尺寸为 $$(dx,dy)$$的物体，放置在深度为 $$z$$的位置，那么在相平面上，它的像素大小为 $$(fx \cdot \frac{dx}{z},fy \cdot \frac{dy}{z})$$，对么对于车道线某一段焦距越小，它的点集越集中，修复效果越好。

### 1.3 高斯球半径修改
高斯球半径修改的目的是为了更改点云图中近处高斯点的大小，从而填补无染色部分。
在原始代码中，
```
scales = scales * z / ixt[0, 0]
```
即每一个高斯点不管矩阵原因，它在相平面上的大小一致，因为它的像素大小为 $$scale \cdot \frac{dx}{z} = scale_{init}$$。
我们的目标是将近处的点放大，可以如下修改：
```
scales = scales * (1 + 1 / (z / 10 + 0.5))
```

## 2. 实验结果
### 2.1 原始参数
即waymo数据集相机参数。

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/7961f803-8caa-4e08-a7eb-5bc242dcebce" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/ecd92bc3-2f56-43ae-a328-996f8ff8de65" />
</div>
<div align=center> 
  Fig.1 原始相机参数图例
</div>

### 2.2 调整俯仰角
相机0安装位置的俯仰角为0.05，其余为0.1。

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/0f3aca53-a1ed-454d-8da4-e03bf2231128" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/58a71997-7e78-41e7-9932-02253bb1cb54" />
</div>
<div align=center> 
  Fig.2 调整俯仰角图例
</div>

### 2.3 改变内参/分辨率
所有相机的内参矩阵都为:

$$
\begin{pmatrix}
 1252.813 & 0 & 826.588 \\
0 & 1252.813 & 469.985 \\ 
0 & 0 & 1
\end{pmatrix}
$$

前风挡(0)位置相机分辨率为1600x896，其余位置相机分辨率为1600*840。

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/05fb1131-73d8-44f4-ae5e-1855dbf71729" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/09768061-08bf-4dec-9158-f0fb165c9991" />
</div>
<div align=center> 
  Fig.3 改变内参/分辨率图例
</div>

### 2.4 更改高斯球半径
半径更改公式为：
```
scales = scales * (1 + 1 / (z / 10 + 0.5))
```

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/68109888-9a2f-4ce8-8c40-f884cf2d7a2a" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/0776d560-446e-4981-9e8f-12f82566418b" />
</div>
<div align=center> 
  Fig.4 更改高斯球半径图例
</div>

### 2.5 整体优化
相机0安装位置的俯仰角为0.05，其余为0.1。
所有相机的内参矩阵都为:

$$
\begin{pmatrix}
 1252.813 & 0 & 826.588 \\
0 & 1252.813 & 469.985 \\ 
0 & 0 & 1
\end{pmatrix}
$$

前风挡(0)位置相机分辨率为1600x896，其余位置相机分辨率为1600*840。

半径更改公式为：
```
scales = scales * (1 + 1 / (z / 10 + 0.5))
```

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/168465ac-64aa-45a7-9ca6-f841645375fc" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/f032483e-52e4-43a7-b115-8f8121cc7470" />
</div>
<div align=center> 
  Fig.5 整体优化图例
</div>

## 3. 修复效果
修复效果示例如下：

<div align=center> 
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/6656ba82-cb6f-44cd-ae7d-3a1e6c2e4878" />   
  <img height="225ptx" alt="image" src="https://github.com/user-attachments/assets/a0ad5f2c-8e49-4d1b-9ad1-66e65d58c391" />
</div>
<div align=center> 
  Fig.6 修复效果图例
</div>

