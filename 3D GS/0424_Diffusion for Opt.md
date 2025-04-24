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


