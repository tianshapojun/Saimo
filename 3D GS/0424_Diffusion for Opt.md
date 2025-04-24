# 基于扩散模型的图像优化器
通过基于扩散模型的图像优化模块来进行数据增强，提升自定义场景数据质量，修复消除场景重建伪影以达到增强训练数据，实现提升重建模型精度与鲁棒性的目的。

## 1. 训练框架
基于 [**Paper**](https://arxiv.org/abs/2403.12036) 进行img2img的图像优化过程，其网络框架如下：

<div align=center>
<img src="https://github.com/user-attachments/assets/335e3daf-d0d5-4579-8571-d25fdf137a66" width="750px">
</div>


算法包含了2种训练方式，pix2pix-turbo和CycleGAN-Turbo，前者通过配对数据训练即img和img是一一对应的(轮廓图和彩色图)，后者通过非配对数据训练达到领域迁移(白天自驾场景和晚上自驾场景)。对于三维重建，上述2种训练方式都可以达成：
> 配对训练，低质图像(未充分训练)和高质图像；

> 未配对训练，低质图像(新视角图像)和高质图像；

## 2. 训练结果
### 2.1 未配对训练

新视角图像为主车平移1m/2m后压缩为424x128(显存原因)，样本示例和修复结果如下：

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/90f2f34e-e36e-4bf4-a04d-f56f5e44c531" width="350px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;001.png</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/eafaa848-59ef-4c38-a04d-be6172838e04" width="350px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;002.gif</font>
      </center>
    </td>
  </tr>
</table>

**可以看到修复起了一部分作用：地面和交通标识补全了部分信息，但是在清晰度上没有明显的改善。**

### 2.2 配对训练
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


