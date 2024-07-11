
# 1. 优化动态物体建模效果
针对动态物体伪影、误识别等现象进行优化。
## 1.1 技术路线
通过对静态背景和动态物体分别建模，共同渲染之后构建损失函数。

对于动态物体，通过对已知物体三维包围盒坐标的二维图像映射掩码与动态模型的渲染结果，构建像素级的交叉熵损失。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(Image, Image_{gt})) + \lambda_{dyn} * CrossEntropy(Image_{dyn},Image_{mask})$

## 1.2 总体效果

(左上) GT；           
(左中) 训练集；         
(左下) 动态物体；       
(右上) x/y拉近5m；  
(右中) 向左变道；  
(右下) 前方两辆车；  

https://github.com/tianshapojun/Saimo/assets/10208337/94060d0e-4db2-46d7-a3d8-7a3daa99d30d

(上上) 训练集；  
(上中) 动态物体；   
(中) 静态；  
(下中) 平移10米；  
(下下) 平移10米上升2米；  

https://github.com/tianshapojun/Saimo/assets/10208337/61c5135d-1e64-4e8c-a2ee-a1aaeb33c0da

# 2. 优化静态背景深度信息
对于静态背景，baseline仅对图像定义了重建损失，以达到渲染后的图像与原图保持一致。当对动态物体进行平移等操作时，由于动态/静态高斯点相对位置不明确出现动态物体缺失等现象，对此进行优化。

## 2.1 技术路线
对于静态背景，通过已知点云映射的深度图，构建像素级的L1损失。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(Image, Image_{gt})) + \lambda_{dyn} * CrossEntropy(Image_{dyn},Image_{mask}) + \lambda_{depth} * L_{depth}$

## 2.2 总体效果
### 2.2.1 优化对比
下图车辆经过平移(驶向行人区域)，优化前与优化后的动态物体细节。

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/0b52d582-47d8-4e7a-b7c2-2d70008a7dfb" width="750px">

整体视频如下，

https://github.com/tianshapojun/Saimo/assets/10208337/dfdf105b-4c24-4de5-9e7a-cad9387b977e

上述视频中的深度图的不平滑主要是由于输入深度图的稀疏性(点云的分布)有关，

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/4441011d-9307-452a-b53a-59a74538e578" width="500px">

### 2.2.2 车辆复制
将上述车辆复制并改变轨迹，

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/da87e9be-44e0-40ed-adfc-01359f6a0a15" width="1000px">


