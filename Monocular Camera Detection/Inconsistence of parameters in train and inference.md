# 感知：训练与推理内外参不一致问题

## 1. 问题描述

对于感知算法，由于训练时相机的内参1(分辨率、 $f_x$、 $f_y$)、外参1(相机坐标到车辆坐标)与推理时的参数2两者往往不一致，将推理时图片通过简单的裁剪、resize、填充后作为模型的输入，
之后通过内外参2进行bbx(车道线)的坐标映射时，会出现整体偏移、物框对应错误的现象。**(下图为resize图片输入模型推理映射后的结果)**

<div align=center>
<img src="https://github.com/user-attachments/assets/141d6632-efd7-4976-9d4d-a87f283885df" width="400px">
</div>

> 上述的问题不可避免，为了使得推理结果更加精确，我们提出了相机映射的方案。

## 2. 相机映射 

相机映射，即根据推理时的图像映射到满足训练时内外参的图像的方法，主要包含2个部分：内参不同和外参不同。

### 2.1 内参不同
为了简化，假设 $f_x=f_y$，内参1包含 $f_1,u_1,v_1$，内参2包含 $f_2,u_2,v_2$，外参两者一致，

$$
u_{train} = f_1 * \frac{x}{z} + u_1, v_{train} = f_1 * \frac{y}{z} + v_1, 
$$

$$
u_{eval} = f_2 * \frac{x}{z} + u_2, v_{eval} = f_2 * \frac{y}{z} + v_2,
$$

根据上述公式，推理时的情景如果用训练时的相机拍摄，其 $(u_{train},v_{train})$像素点的颜色由推理图像 $(f_2 * \frac{u_{train}-u_1}{f_1} + u_2, f_2 * \frac{v_{train}-v_1}{f_1} + v_2)$位置的像素点决定，
由于运算结果不一定为整数可用双线性插值计算。

将映射后的图像输入至模型即可，**效果如下：**

<div align=center>
<img src="https://github.com/user-attachments/assets/e02adddd-d671-4a98-9d5d-7eda8ee36b60" width="400px">
</div>

### 2.2 外参不同
外参问题主要是两者安装高度不一致导致并且常常发生在车道线检测，2D图像上的车道线和肉眼观察的车道线即使一致，但如果高度预估错误的话将可能导致相对位置在图像和BEV视角相悖。**具体如下图所示(在FOV视角车道线和车辆不重叠，在BEV视角两者重叠)**

<div align=center>
<img src="https://github.com/user-attachments/assets/0200ffa0-7d0d-4be1-a72c-91b950190d1e" width="400px">
</div>

为了简化，假设 $f_x=f_y$，内参两者一致，外参的差别在于相机安装的高度(已知)，

$$
u_{train} = f_1 * \frac{x}{z} + u_1, v_{train} = f_1 * \frac{y_1}{z} + v_1, 
$$

$$
u_{eval} = f_1 * \frac{x}{z} + u_1, v_{eval} = f_1 * \frac{y_2}{z} + v_1,
$$

根据上式子，可以得到 $u_{train} = u_{eval}$， $v_{train}$和 $v_{eval}$之间的关系式可以有2种表达方式：

$$
v_{eval} = v_{train} + f_1 * \frac{y_2 - y_1}{z},  (1)
$$

$$
v_{eval} = f_1 * \frac{v_{train}-v_1}{f_1} * \frac{y_2}{y_1} + v_1, (2)
$$

对于公式(1)，未知数为z(距离)，很难得到；对于公式(2)，未知数为y(车道线对应的地面高度，因为道路不一定是平整的)，相较而言根据公式(2)加上高度假设，能够作出推理；

**效果如下：**

<div align=center>
<img src="https://github.com/user-attachments/assets/ddff703a-2e3a-415e-a7f7-89e1776de46e" width="400px">
<img src="https://github.com/user-attachments/assets/b8f87f64-d7ea-48f2-b424-039dd1e1b3d9" width="400px">
</div>

## 2.3 内外参都不同

将2.1节内容和2.2节内容结合即可。
