# 1. 技术路线
通过对静态背景和动态物体分别建模，共同渲染之后构建损失函数。

$L_{total} = (1.0 - \lambda_{dssim}) * L_{l1} + \lambda_{dssim} * (1.0 - ssim(image, image_{gt}))$

# 2. 效果展示
## 2.1 总体效果
视频分上中下三行:
- 第一行为ground truth
- 第二行为baseline还原效果
- 第三行为混合建模还原效果

https://github.com/tianshapojun/Saimo/assets/10208337/4216c7aa-c5b9-4c69-b6dc-8287af20cfe1

## 2.2 静态/动态效果
现象：
- 将部分天空和地面当作动态建模目标

优化：
- 限制动态模型高斯点坐标位置
- 添加损失函数项(per-pixel softmax cross-entropy loss between rendered semantic logits and input 2D semantic segmentation predictions)

https://github.com/tianshapojun/Saimo/assets/10208337/8a86e0f8-cd91-4201-b0a5-c1a1b068a74f








