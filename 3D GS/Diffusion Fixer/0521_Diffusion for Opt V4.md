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

<div align=center>
<img src="https://github.com/user-attachments/assets/d0e83475-d5e3-4cb3-86aa-fe1c437bf8a4" width="1000px">
<img src="https://github.com/user-attachments/assets/e2c788eb-298f-48f9-bc04-a4385da73911" width="1000px">
<img src="https://github.com/user-attachments/assets/75dd49a9-81e5-4137-9734-286efb4c4ce0" width="1000px">
</div>

### 2.2 指标分析
通过PSNR、SSIM进行量化的指标计算，比较上述实验结果，共选取了测试集6个场景共239张图片；

| Eeperiment   |   Batch |   PSNR |   SSIM |  
|:----------|--------------:|----------:|----------:|
| Exp1 (basic)  |   20000 |     23.01 |      0.65 |  
| Exp1 (basic)  |   41000 |     23.52 |      0.66 |
| Exp2 (L1 loss)  |   20000 |     22.66 |      0.65 |  
| Exp3 (Style loss)  |   20000 |      22.91 |      0.64 |   

从数值结果来看，以MSE作为重建损失效果更好，添加了style loss略微较低了指标水平；

---

选取相同测试集，比较当前修复器和streetcrafter中修复器的表现效果
| Eeperiment   |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |
|:----------|----------:|------:|----------:|----------:|----------:|----------:|----------:|----------:|
| Exp1 (41000)  |   Waymo049 |     **26.01** |      **0.75** |   **0.22** |   Waymo176 |     **22.47** |      0.61 |     0.27 |  
| StreetCrafter  |  Waymo049 |     25.26 |      **0.75** |   0.28 |   Waymo176 |     21.60 |      **0.69** |     **0.23** |

从指标上看，两者各有优劣，但观察具体图像，streetcrafter的输出在轮廓边缘上更清晰线条更突出；

<div align=center>
<img src="https://github.com/user-attachments/assets/aef0a8c1-fa70-4f4a-9e3b-73e3c6615925" width="1000px">
<img src="https://github.com/user-attachments/assets/b6d8b4e7-78f0-49ae-8997-b3f53422747b" width="1000px">
</div>

---

## 3. 总结与未来方案
- 调整训练参数，例如learning rate/各个损失的比重；
- 如果一步去噪提升有限，是否考虑两步去噪？
- 将text_embedding替换为image_embedding ([StreetCrafter](https://arxiv.org/abs/2412.13188))；
- 添加reference mixing layer ([DIFIX3D+](https://arxiv.org/pdf/2503.01774?));
