# 1. 多动态物体建模实现
针对多个动态物体，由于其外形不同(即高斯椭球不同)、位置/角度不同(即转换矩阵不同)，原本建模不适用，因此进行更新优化。
## 1.1 技术路线
如N个物体，初始化MN个高斯点，增量高斯球标签变量，之后每一帧图片根据标签进行对应的坐标变换。

## 1.2 效果展示

https://github.com/user-attachments/assets/ade29974-3360-4039-a85f-8162b08f7f13

## 1.3 技术细节
- 标签文件需要提供目标物的id，从而获得完整轨迹；
- 若某id在某帧缺失标签，则旋转矩阵设为0，平移向量为[-9999,-9999,0]，即物体不在图像中出现；
- 由于高斯球标签变量，能够较好区分不同动态物体，以便后泛化操作；

# 2. 动态物体建模优化
## 2.1 坐标变换
位置变换，已在1中实现(轨迹控制)；

$$
\mu_w = R_t \mu_o + T_t.
$$

旋转变换，实现后在1中数据集上效果不明显，分析是其中车辆全程直行，和旋转相关性不大，还有可能的原因是训练出的椭球在相应坐标轴上具有旋转不变性；

$$
R_w = R_o R_t^T.
$$

## 2.2 刚体对称性

在以车头方向为x轴正向，z轴向上的右手坐标系下，车辆关于xz平面对称，[[AutoSplat](https://arxiv.org/abs/2407.02598)]提出了反射高斯模块 **(下图上)**，和我们设计的基于刚体对称性的对称高斯模块细节略有不同。**(下图下)**

<div align=center>
<img src="https://github.com/user-attachments/assets/ee357360-a7f7-4190-a79e-e23c33efcfdf" width="600px">
</div>

> 在训练阶段，反射高斯模块分别渲染原高斯点图和反射高斯点图并与gt作对比；在推理阶段，仅渲染原高斯点图。

> 在训练和推理阶段，对称高斯模块将原高斯点和对称高斯点混合渲染并与gt作对比，与反射高斯模块相比训练阶段渲染的图像少了一张。

实验结果如下，将红色车辆进行顺时针旋转，由之前训练数据可知红色车辆并没有其右侧信息，初步优化渲染效果提升，迭代优化中。

<div align=center>
<img src="https://github.com/user-attachments/assets/8baaa4e5-b1be-4360-86a5-45a0e2936dd3" width="600px">
</div>
