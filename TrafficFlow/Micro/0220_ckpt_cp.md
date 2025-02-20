对于微观交通流模型，在训练数阶段加入大量“真实”数据后，对模型效果的影响进行阶段性评估。
# 0. 总结
> **1. 模型1和2在直道和8字型基本能沿车道行走，模型3出现碰撞、冲出车道等现象；**    
> **2. 可能产生上述现象的原因：1.训练不够充分；2.数据污染；**

## 1. 实验设置
比较下述3种ckpt在相同地图相同随机数种子下环境车的表现，三者的差别为训练数据：    
1. (目前线上) micro_model_0920_10f_20.pth，通过仿真数据+部分dz/hz真实数据；
2. (0220训练) 仿真数据，样本构建较为稀疏；
3. (0217训练，中间状态，**还未达到预设轮次**) 仿真数据+dz/hz/hw真实数据；

## 2. 测试地图和效果
通过直道进行测试；
<div align=center> 
  [1]<img src="https://github.com/user-attachments/assets/981955dc-db00-45fb-8f5f-b84dcaf382a0" width="800px"> 
  
  [2]<img src="https://github.com/user-attachments/assets/4be07b52-8ca6-483c-aa60-97114434d1a3" width="800px">     
  
  [3]<img src="https://github.com/user-attachments/assets/661d42e5-f3cc-405c-ac66-1564d1040d4c" width="800px"> 
</div>

通过8字地图进行测试；
<div align=center> 
  [1]<img src="https://github.com/user-attachments/assets/4bbd0c26-9281-4251-bb87-95425c3daa74" width="600px"> 
  
  [2]<img src="https://github.com/user-attachments/assets/e72d1165-5617-4161-bd4d-0d1c4e2406d1" width="600px">     
  
  [3]<img src="https://github.com/user-attachments/assets/3d4abcad-e656-413e-a674-904486c02e7c" width="600px"> 
</div>







