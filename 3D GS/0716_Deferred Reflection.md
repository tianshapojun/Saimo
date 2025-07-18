# 三维重建中延迟反射相关实验记录
经典的Phong 光照模型是用于模拟真实世界中的光照效果，它将光照分为环境光(Ambient)、漫反射光(Diffuse) 和镜面反射光(Specular) 三个部分。
[3DGS-DR](https://arxiv.org/abs/2404.18454) 提出了一种基于延迟着色的方法，利用环境贴图反射模型实现镜面反射，最终的效果为传统的3d-gs 渲染图层+ 延迟反射通道的线性叠加。

将该部分内容嵌入至已有的框架后，本文将对相关实验结果作总结分析。

## 1. 整体方案
在[3DGS-DR](https://arxiv.org/abs/2404.18454)的设计中没有涉及动静结合、天空模型、深度预测等模块，无法支持当前需求，所以将其环境贴图合并到当前结构中。
值得注意的是，目前使用的三维重建渲染器基于[gsplat](https://github.com/nerfstudio-project/gsplat)项目，支持rgb渲染、深度渲染等；
[3DGS-DR](https://arxiv.org/abs/2404.18454)使用的渲染器包括[diff-gaussian-rasterization_c3](https://github.com/gapszju/3DGS-DR/tree/main/submodules/diff-gaussian-rasterization_c3)
和[diff-gaussian-rasterization_c7](https://github.com/gapszju/3DGS-DR/tree/main/submodules/diff-gaussian-rasterization_c7)，
后者支持rgb渲染、法向量渲染和反射强度渲染(即镜面反射图层)等。

结合上述信息，可行的方案包括：
> baseline，渲染图层(gsplat);   
> 方案1，渲染图层(c7) + 镜面反射图层(c7);   
> 方案2，渲染图层(gsplat) + 镜面反射图层(c7);

## 2. 实验结果
### 2.1 指标分析
| Eeperiment   |   Batch |  # Scenes | PSNR(↑) |   SSIM(↑) |
|:----------|--------------:|----------:|----------:|----------:|
| baseline   |   30000 |  121 | 26.94  |    0.81   |
| 方案1   |   30000 |  121 | 24.73  |     - |
| 方案2   |   30000 |   121 | 26.75  |     0.81 | 

---

通过指标来看，baseline和方案2结果相差不大，而方案1的渲染效果较差。

### 2.2 envmap渲染效果

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/1f946904-e3b8-4e1f-bd1a-9420b611b25e" height="150px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;Iteration:1000.png</font>
      </center>
    </td>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/5edb5906-415d-4016-80c6-cf789e05f889" height="150px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;Iteration:7000.png</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/6fae5154-b935-4d29-a0a4-81e6d9e9e907" height="150px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;Iteration:10000.png</font>
      </center>
    </td>
    <td>
      <center>
        <img src="https://github.com/user-attachments/assets/8a21f6ec-f37b-4d88-a5ad-679cc2ba38d9" height="150px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;Iteration:27000.png</font>
      </center>
    </td>
  </tr>
</table>

---

上图为不同训练阶段envmap的渲染结果，可以看到随着训练轮数增加环境图层逐渐退化为空白图，最终图像只受原始图层影响。

下图为原始文献中训练的图像(360°环绕的小轿车)和最终训练得到的环境图，可以较清晰地看见树木和房屋地倒影构成了环境图层的主体。

---

<div align=center>
<img src="https://github.com/user-attachments/assets/9fafc532-449e-49c6-ae03-d7b254690dcf" width="800px">
</div>

## 总结和改进方向
> a. 本次实验主要将[3DGS-DR](https://arxiv.org/abs/2404.18454)中关于镜面反射图层的模块移植到了现有的框架中进行训练。结果是随着训练轮数增加环境图层逐渐退化为空白图，最终图像只受原始图层影响。针对此现象，有如下分析：   
> 1. 动态的环境车镜面反射的效果不仅仅和入射光、法向量有关，还和其所在位置有关(例如在A点反射的是其它车辆，在B点发射的是周围建筑物)，和目前设计中的环境光反射原理不一致；(**修改环境贴图模型，与反射光和反射位置关联**)   
> 2. 由于动态车占比较小且收集到的数据并非360°环视，对环境光获取的信息不充分；(**针对环境光关注区域，增加损失权重**)

> b. 原始文献中额外输入了两个参数：env_scope_center和env_scope_radius，分别表示关注的镜面反射区域的中心点和半径。在代码移植中，将此区域转化为动态物体所在区域。和原始文献相比，镜面反射区域**由图像中的绝大部分变为了小部分**，**由静止的区域变为了动态的区域**；
