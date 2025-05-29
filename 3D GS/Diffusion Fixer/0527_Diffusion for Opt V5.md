# 基于扩散模型的图像优化器 V5
通过基于扩散模型的图像优化模块来进行数据增强，提升自定义场景数据质量，修复消除场景重建伪影以达到增强训练数据，实现提升重建模型精度与鲁棒性的目的。

## 1. 训练优化方向
根据之前实验，baseline的部分模块如下：
> a. 通过点云图映射图像+参考图像作为模型输入，   
> b. 点云图通过encoder的输出和参考图的encoder后接cross-attention进行elementwise求和进入U-net网络，   
> c. 损失函数加入图像梯度损失，   

根据参考文献，做出了如下尝试；
- 实验0，baseline；
- 实验1，模型训练输入从点云图调整为未充分训练的图像(背景修复效果提升难度大)；
- 实验2，模型训练输入从点云图调整为未充分训练的图像(上半部分特征)+点云图(下半部分特征)；

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/e60d6e09-cc26-4b3e-9e3f-e21fe5abb8d1" height="350px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;实验0输入.png</font>
      </center>
    </td>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/51562346-9ace-4f8b-a85e-0623b9e3870c" height="350px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;实验1输入.png</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/3e1149f0-d9df-4aa2-9be9-8e21a50f171a" height="350px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;实验2输入.png</font>
      </center>
    </td>
  </tr>
</table>

## 2. 结果验证
### 2.1 原始轨迹
主要介绍了修复效果以及对应的指标计算结果。
#### 2.1.1 修复后的图像
经过一定次数训练后，效果图如下(从上至下四张图分别对应实验0、1、2、3和StreetCrater修复器)：
> 实验0的训练batch=20000，实验1的训练batch=10000，实验2的训练batch=6000；   
> 三个实验的batch_size都为1；   
> 实验1、2相比较base实验在背景修复效果上提升巨大；

<div align=center>
    
  --- 
  
  <img src="https://github.com/user-attachments/assets/272fdef3-8a38-4c54-a0a6-349ff772db38" width="1000px">
  <font color="AAAAAA">实验0样例输出.png</font>
  
  --- 
  
  <img src="https://github.com/user-attachments/assets/ae5d5638-61a2-4ee1-ba5b-a88098ad4526" width="1000px">
  <font color="AAAAAA">实验1样例输出.png</font>
    
  --- 
  
  <img src="https://github.com/user-attachments/assets/8e6bc444-2ae7-44b1-a20a-dafea66a4536" width="1000px">
  <font color="AAAAAA">实验2样例输出.png</font>
    
  --- 
  
  <img src="https://github.com/user-attachments/assets/b6d8b4e7-78f0-49ae-8997-b3f53422747b" width="1000px">
  <font color="AAAAAA">StreetCrater修复器样例输出.png</font>
    
  --- 
  
</div>


#### 2.1.2 指标分析
通过PSNR、SSIM进行量化的指标计算，比较上述实验结果，共选取了测试集6个场景共100张图片；

| Eeperiment   |   Batch |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) |  
|:----------|--------------:|----------:|----------:|----------:|
| Exp0   |   20000 |    24.53  |    0.78   |   0.46    |  
| Exp1   |   10000 |    **27.62**  |     **0.82** |   0.37   |
| Exp1   |   6000 |    **27.62**  |     **0.82** |   0.37   |
| StreetCrafter   |   --- |   26.21   |   **0.82**    |   **0.35**    |  

从数值结果来看，加入了图像梯度损失后修复效果更佳，以实验2的参数配置二步去噪的结果比较一步去噪没有明显提升；

---
### 2.2 视角平移
主要介绍了修复效果以及对应的指标计算结果。
#### 2.2.1 修复后的图像
经过一定次数训练后，效果图如下(上中下分别对应实验?)：
> 实验1相比较base实验在背景修复效果上提升巨大；   
> 实验1的数据较依赖于未充分训练的图像，即输入图像伪影、色散情况较严重，修复图目前无法修正，但此状况可以通过迭代训练来减弱或回避；
选取相同测试集，比较当前修复器和streetcrafter中修复器的表现效果

| Eeperiment   | Batch  |   DataSet |   PSNR(↑) |   SSIM(↑) |    LPIPS(↓) | 
|:----------|----------:|------:|------:|----------:|----------:|
| Exp0 (20000)  |20000 |   Waymo049 |      **25.57**|       0.75|    **0.22**|
| Exp1 (20000)  |10000 |   Waymo049 |      25.49|       0.75|    0.22|  
| Exp1 (20000)  |10000 |   Waymo049 |      25.42|       **0.76**|    0.24| 
| StreetCrafter  |--- |  Waymo049 |      25.26|       0.75|    0.28|  

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
- 模型训练输入从点云图调整为未充分训练的图像(背景修复效果提升难度大)；

## 补充
streetcrafter修复器输出80张图片耗时约22分钟，当前修复器耗时约1分钟。

---

https://github.com/user-attachments/assets/59c1762f-971b-4dc1-9ea4-f01267226f23
