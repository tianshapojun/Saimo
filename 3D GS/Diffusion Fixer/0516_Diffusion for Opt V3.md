# 基于扩散模型的图像优化器 V3
通过基于扩散模型的图像优化模块来进行数据增强，提升自定义场景数据质量，修复消除场景重建伪影以达到增强训练数据，实现提升重建模型精度与鲁棒性的目的。

## 1. 训练优化方向
根据之前实验，通过点云图映射图像+参考图像作为模型输入，通过encoder的输出进行elementwise求和进入U-net网络，根据参考文献，做出了如下尝试；
- 实验1，baseline，点云图映射图像+参考图像；
- 实验2，重建损失由MSE改为L1损失；
- 实验3，加入基于Vgg网络特征的style loss ([DIFIX3D+](https://arxiv.org/pdf/2503.01774?))，通过计算Gram matrix得到,具体如下；
  
$$ 
L_{Gram} = \frac{1}{L} \sum_{l=1}^{L} \beta_l \Vert G_l(\hat{I}) - G_l(I)\Vert_2, 
$$

$$
G_l(I) = \phi_l(I)^T \phi_l(I).
$$

## 2. 训练结果
### 2.1 仅点云映射图

> (训练配置default)--lambda_clipsim=5.0 --lambda_l2=1.0 --lambda_lpips=5.0 --lambda_gan=0.5

修复后的图像如下：

<div align=center>
<img src="https://github.com/user-attachments/assets/63d41bd9-3363-43a5-8350-1bb6440faac9" width="350px">
<img src="https://github.com/user-attachments/assets/db914ce1-57ce-4062-907a-e9cecaad5590" width="350px">
</div>

### 2.2 点云映射图+参考图像

> (训练配置)--lambda_clipsim=0.0 --lambda_l2=5.0 --lambda_lpips=1.0 --lambda_gan=0.0；   
> 训练样本在高度上将点云图和参考图在Height维度进行拼接，即输入为 **(B, C, 2xH, W)**；   
> 由于输入和输出图像形状一致，取上半部分张量作为评估；

修复后的图像如下：

<div align=center>
<img src="https://github.com/user-attachments/assets/36814cb7-2035-42ab-8147-c3c7e9b632ff" width="350px">
<img src="https://github.com/user-attachments/assets/9d727f17-696d-45f7-9557-7b438679d756" width="350px">
</div>


## 3. 总结与未来方案

- 从训练的中间/最终结果来看，点云映射+参考图像的训练输入表现更好，图像中车道线和车辆轮廓整体较为清晰，车辆/环境物/天空细节模糊/缺失，该部分内容在点云图上没有体现，从参考图的拼接上看并没有很好的补充；
- 可参考的方案：将点云图和参考图经过encoder的输出进行elementwise求和；
- 将text_embedding替换为image_embedding；

## 补充内容
> 将点云图和参考图经过encoder的输出进行elementwise求和的效果如下：   
> 左图为高度拼接，右图为特征求和，都经过8000轮次的训练；   
> 修复效果较之前相比有所提高，在图片上半部分点云未能投影的区域展现了更多细节；

<div align=center>
<img src="https://github.com/user-attachments/assets/0d9dc404-a596-4452-882c-c50804fbc1a6" width="500px">
<img src="https://github.com/user-attachments/assets/5dd75f21-2533-4ed8-82cc-ccca1f8da944" width="500px">
<img src="https://github.com/user-attachments/assets/886bde47-7a30-45bb-aae2-471f5454c1a1" width="500px">
<img src="https://github.com/user-attachments/assets/5486ab81-ef3c-4452-b174-c5c21c899952" width="500px">
</div>
