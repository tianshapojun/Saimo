# 1. 动静联合建模v1.0
## 1.1 技术路线
通过对静态背景和动态物体分别建模，共同渲染之后构建损失函数。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(image, image_{gt}))$

## 1.2 效果展示
### 1.2.1 总体效果
彩色图，视频分上中下三部分:
- 第一行为ground truth
- 第二行为baseline还原效果
- 第三行为混合建模还原效果

https://github.com/tianshapojun/Saimo/assets/10208337/4216c7aa-c5b9-4c69-b6dc-8287af20cfe1

深度图，视频分为上下两部分：
- 第一行为baseline深度图
- 第二行为混合建模深度图

https://github.com/tianshapojun/Saimo/assets/10208337/4ff816fd-4f7a-42a3-b343-302474c46f29

### 1.2.2 静态/动态效果
现象：
- 将部分天空和地面当作动态建模目标

优化：
- 限制动态模型高斯点坐标位置
- 添加损失函数项(per-pixel softmax cross-entropy loss between rendered semantic logits and input 2D semantic segmentation predictions)

https://github.com/tianshapojun/Saimo/assets/10208337/8a86e0f8-cd91-4201-b0a5-c1a1b068a74f

# 2. 动静联合建模v2.0
## 2.1. 优化动态物体建模效果
针对动态物体伪影、误识别等现象进行优化。
### 2.1.1 技术路线
通过对静态背景和动态物体分别建模，共同渲染之后构建损失函数。

对于动态物体，通过对已知物体三维包围盒坐标的二维图像映射掩码与动态模型的渲染结果，构建像素级的交叉熵损失。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(Image, Image_{gt})) + \lambda_{dyn} * CrossEntropy(Image_{dyn},Image_{mask})$

### 2.1.2 总体效果

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

## 2.2 优化静态背景深度信息
对于静态背景，baseline仅对图像定义了重建损失，以达到渲染后的图像与原图保持一致。当对动态物体进行平移等操作时，由于动态/静态高斯点相对位置不明确出现动态物体缺失等现象，对此进行优化。

### 2.2.1 技术路线
对于静态背景，通过已知点云映射的深度图，构建像素级的$L_1$损失。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(Image, Image_{gt})) + \lambda_{dyn} * CrossEntropy(Image_{dyn},Image_{mask}) + \lambda_{depth} * L_{depth}$

### 2.2.2 总体效果
#### 2.2.2.1 优化对比
下图车辆经过平移(驶向行人区域)，优化前与优化后的动态物体细节。

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/0b52d582-47d8-4e7a-b7c2-2d70008a7dfb" width="750px">

整体视频如下，

https://github.com/tianshapojun/Saimo/assets/10208337/dfdf105b-4c24-4de5-9e7a-cad9387b977e

上述视频中的深度图的不平滑主要是由于输入深度图的稀疏性(点云的分布)有关，

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/4441011d-9307-452a-b53a-59a74538e578" width="500px">

#### 2.2.2.2 车辆复制
将上述车辆复制并改变轨迹，

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/da87e9be-44e0-40ed-adfc-01359f6a0a15" width="1000px">
