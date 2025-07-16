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
