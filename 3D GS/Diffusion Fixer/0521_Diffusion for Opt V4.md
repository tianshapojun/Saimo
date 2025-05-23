# 基于扩散模型的图像优化器 V4
通过基于扩散模型的图像优化模块来进行数据增强，提升自定义场景数据质量，修复消除场景重建伪影以达到增强训练数据，实现提升重建模型精度与鲁棒性的目的。

## 1. 训练优化方向
根据之前实验，通过点云图映射图像+参考图像作为模型输入，通过encoder的输出进行elementwise求和进入U-net网络，根据参考文献，做出了如下尝试；
- 实验0，baseline；
- 实验1，由直接elementwise求和变为参考图的encoder接self-attention后elementwise求和；
- 实验2，实验1+一步去噪改为二步去噪；
- 实验3，实验1+图像梯度损失；
  
$$ 
L_{gradient} = \frac{1}{N} \sum_{l=1}^{N} \left\| \nabla \hat{I} - \nabla I \right\|_1, 
$$

## 2. 训练结果
### 2.1 修复后的图像
经过20000次优化后，效果图如下(上中下分别对应实验123)：
> 通过观察，实验3在物体边缘上比实验1和实验2效果更优，后两者肉眼观察效果难以区分；
> 实验3在上半部分(无点云图输入)的图像修复效果不佳，随着训练轮数的增加改善不大；

<div align=center>
<img src="https://github.com/user-attachments/assets/99376329-f007-4925-b856-193c6d14627a" width="1000px">
<img src="https://github.com/user-attachments/assets/053848b9-78ba-435c-a7c4-aa155e6d38ab" width="1000px">
<img src="https://github.com/user-attachments/assets/272fdef3-8a38-4c54-a0a6-349ff772db38" width="1000px">
</div>

### 2.2 指标分析
通过PSNR、SSIM进行量化的指标计算，比较上述实验结果，共选取了测试集6个场景共239张图片；

| Eeperiment   |   Batch |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |  
|:----------|--------------:|----------:|----------:|----------:|
| Exp0   |   20000 |     23.01 |      0.65 |      0.30 |  
| Exp1   |   20000 |     23.07 |      0.66 |      **0.27** |
| Exp2   |   20000 |     23.05 |      0.65 |      0.28 |  
| Exp3   |   20000 |     **23.13** |      **0.68** |      0.30 |   

从数值结果来看，加入了图像梯度损失后修复效果更佳，以实验2的参数配置二步去噪的结果比较一步去噪没有明显提升；

---

选取相同测试集，比较当前修复器和streetcrafter中修复器的表现效果
| Eeperiment   |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |
|:----------|----------:|------:|----------:|----------:|----------:|----------:|----------:|----------:|
| Exp1 (20000)  |   Waymo049 |      **25.57**|       0.75|    **0.22**|   Waymo176 |      22.25|       0.61|      0.27|
| Exp2 (20000)  |   Waymo049 |      25.49|       0.75|    0.22|   Waymo176 |      22.25|       0.60|      0.28|
| Exp3 (20000)  |   Waymo049 |      25.42|       **0.76**|    0.24|   Waymo176 |      **22.35**|       0.64|      0.31|
| StreetCrafter  |  Waymo049 |      25.26|       0.75|    0.28|   Waymo176 |      21.60|       **0.69**|      **0.23**|

---

在代码中，streetcrafter在计算修复器和生成图的损失时，只截取了图片的下半部分
```
image[:, upper:, :]
upper = int(image.shape[-2] * 0.4))
```
因此我们评估裁剪后图片的相应指标：

| Eeperiment   |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |
|:----------|----------:|------:|----------:|----------:|----------:|----------:|----------:|----------:|
| Exp1 (20000)  |   Waymo049 |      26.12|       0.76|    **0.22**|   Waymo176 |      23.97|       0.71|      **0.24**|
| Exp2 (20000)  |   Waymo049 |      26.21|       0.75|    0.23|   Waymo176 |      23.80|       0.69|      0.25|
| Exp3 (20000)  |   Waymo049 |      26.36|       0.76|    0.24|   Waymo176 |      **24.38**|       0.73|      0.25|
| StreetCrafter  |  Waymo049 |      **27.06**|       **0.81**|    0.29|   Waymo176 |      22.58|       **0.75**|      **0.24**|

---

从指标上看，两者各有优劣，但观察具体图像，streetcrafter的输出对物体的细节尤其是远处物体有很好的还原;

<div align=center>
<img src="https://github.com/user-attachments/assets/272fdef3-8a38-4c54-a0a6-349ff772db38" width="1000px">
<img src="https://github.com/user-attachments/assets/b6d8b4e7-78f0-49ae-8997-b3f53422747b" width="1000px">
</div>

---

## 3. 总结与未来方案
- 将text_embedding替换为image_embedding ([StreetCrafter](https://arxiv.org/abs/2412.13188))；

## 补充
streetcrafter修复器输出80张图片耗时约22分钟，当前修复器耗时约1分钟。

https://github.com/user-attachments/assets/59c1762f-971b-4dc1-9ea4-f01267226f23


