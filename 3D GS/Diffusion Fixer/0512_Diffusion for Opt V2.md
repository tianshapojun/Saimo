# 基于扩散模型的图像优化器 V2
通过基于扩散模型的图像优化模块来进行数据增强，提升自定义场景数据质量，修复消除场景重建伪影以达到增强训练数据，实现提升重建模型精度与鲁棒性的目的。

## 1. 训练优化方向
- 通过对文献的再阅读，相关文献[StreetCrafter](https://arxiv.org/abs/2412.13188)、[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)、[ReconDreamer](https://arxiv.org/pdf/2411.19548)、[DriveDreamer4D](https://arxiv.org/pdf/2410.13571)在训练优化器时用的是多场景数据(至少8个场景)，而非单一场景；
- 训练样本构建方式更新参照[StreetCrafter](https://arxiv.org/abs/2412.13188)，通过点云图映射图像(训练方式1)；
- 训练样本构建方式更新参照[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)，点云图映射图像+参考图像(训练方式2)；

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/71f4672b-6dae-43bc-ba60-ff633032bf11" height="250px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;训练方式1.png</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/bd060d71-5596-429f-b16b-a73a4d5cd9bb" height="250px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;训练方式2.png</font>
      </center>
    </td>
  </tr>
</table>

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
