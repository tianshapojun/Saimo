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
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;训练方式2.gif</font>
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

> (训练配置)--lambda_clipsim=0.0 --lambda_l2=5.0 --lambda_lpips=1.0 --lambda_gan=0.0

修复后的图像如下：

<div align=center>
<img src="https://github.com/user-attachments/assets/36814cb7-2035-42ab-8147-c3c7e9b632ff" width="350px">
<img src="https://github.com/user-attachments/assets/9d727f17-696d-45f7-9557-7b438679d756" width="350px">
</div>


## 3. 总结与未来方案

- 通过对文献的再阅读，相关文献[StreetCrafter](https://arxiv.org/abs/2412.13188)、[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)、[ReconDreamer](https://arxiv.org/pdf/2411.19548)、[DriveDreamer4D](https://arxiv.org/pdf/2410.13571)在训练优化器时用的是多场景数据(至少8个场景)，而非单一场景——**优化训练数据；**
- 训练样本构建方式更新[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)，包括：Cycle Reconstruction、Model Underfitting、Cross Reference。——**优化训练数据；**
- 作为唯一开源优化器的项目[StreetCrafter](https://github.com/zju3dv/street_crafter)，**进行该优化器的效果验证；**
- [DIFIX3D+](https://arxiv.org/pdf/2503.01774?)在实验阶段比较了pix2pix-turbo和Difix两个优化器的效果，即**验证了pix2pix-turbo的可行性和提供了优化的方向；**
