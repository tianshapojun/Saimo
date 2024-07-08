
# 1. 优化动态物体建模效果
针对动态物体伪影、误识别等现象进行优化。
## 1. 技术路线
通过对静态背景和动态物体分别建模，共同渲染之后构建损失函数。

对于动态物体，通过对已知物体三维包围盒坐标的二维图像映射掩码与动态模型的渲染结果，构建像素级的交叉熵损失。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(Image, Image_{gt})) + \lambda_{dyn} * CrossEntropy(Image_{dyn},Image_{mask})$

## 2. 总体效果

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

