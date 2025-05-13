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




**可以看到修复起了一部分作用：地面和交通标识补全了部分信息，但是在清晰度上没有明显的改善。**

### 2.2 点云映射图+参考图像
损失包含：**Reconstruction loss、CLIP similarity loss、Generator loss and Discriminator loss;**

低质图像从下述2中方式获取1.未充分训练数据；2.真实数据通过2.1中的b2a方式获取。通过多次实验，选取分析下述2中较为典型的训练结果。

#### 2.2.1 训练配置1
> --lambda_clipsim=0 --lambda_l2=10.0 --lambda_lpips=0.0 --lambda_gan=0.0

第一行为输入，第二行为输出，示例如下：

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/1cef5ff0-aa65-4365-ba8a-4e8938d0f082" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Test</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/32b6adcc-3783-498a-ba78-5e57aaa41859" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Left 1.0m</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/f1cb74f6-3918-440e-9e06-f9ec6b17a1ed" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Left 2.0m</font>
      </center>
    </td>
  </tr>
</table>

**可以看到在测试集上效果很好(过拟合)，但在新视角下优化效果出现非常大的差别，初步分析为输入分布不同。**

#### 2.2.2 训练配置2
> (default)--lambda_clipsim=5.0 --lambda_l2=1.0 --lambda_lpips=5.0 --lambda_gan=0.5

第一行为输入，第二行为输出，示例如下：

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/db83cf06-ae5e-4ab3-bafa-7feb5d844a98" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Test</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/36b08b02-92d5-4f5e-8333-eaf243824c36" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Left 1.0m</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/ed875bdb-ae18-4671-a1e8-f17f61aca477" width="300px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Left 2.0m</font>
      </center>
    </td>
  </tr>
</table>

**由于增加了重建损失外其它部分的权重，在测试集上图像质量显著低于配置1，在自定义视角效果也不符合预期。**

## 3. 总结与未来方案

- 通过对文献的再阅读，相关文献[StreetCrafter](https://arxiv.org/abs/2412.13188)、[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)、[ReconDreamer](https://arxiv.org/pdf/2411.19548)、[DriveDreamer4D](https://arxiv.org/pdf/2410.13571)在训练优化器时用的是多场景数据(至少8个场景)，而非单一场景——**优化训练数据；**
- 训练样本构建方式更新[DIFIX3D+](https://arxiv.org/pdf/2503.01774?)，包括：Cycle Reconstruction、Model Underfitting、Cross Reference。——**优化训练数据；**
- 作为唯一开源优化器的项目[StreetCrafter](https://github.com/zju3dv/street_crafter)，**进行该优化器的效果验证；**
- [DIFIX3D+](https://arxiv.org/pdf/2503.01774?)在实验阶段比较了pix2pix-turbo和Difix两个优化器的效果，即**验证了pix2pix-turbo的可行性和提供了优化的方向；**
