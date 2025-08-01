# 相机校准转换 V1
3.1项目的需求是将路采数据的传感器数据转换为标准格式，对于相机来说即外参、内参、图像长宽的转换。根据之前训练的图像修复器对主车轨迹进行左右平移，渲染修复后的图像加入训练效果不理想
，因此改变思路：将标准格式的图像修复后加入样本训练，评估结果。

## 1. 各项比较基线

- 实验0，训练集+左右平移+gs天空模型   
- 实验1，训练集+左右平移+nerf天空模型   
- 实验2，训练集+标准格式(nerf天空模型修复得到)+nerf天空模型
- 实验3，训练集+标准格式(nerf天空模型修复得到)+gs天空模型 

注：不同的天空模型在相机参数变换后效果不同；gs天空模型在原始轨迹、平移轨迹渲染效果较好于nerf天空模型，但在此情况下出现类似于光晕的现象，不如nerf天空模型，**具体如下**；

<div align=center>
    
  --- 
  
  <img src="https://github.com/user-attachments/assets/fc996c9b-292d-48d0-bf1e-0ca4ff866b31" width="1000px">
  <font color="AAAAAA">gs天空模型.png</font>
  
  --- 
  
  <img src="https://github.com/user-attachments/assets/182ba27f-2b6b-4d5b-9e79-5ca117765d7b" width="1000px">
  <font color="AAAAAA">nerf天空模型.png</font>
    
  --- 

</div>
  
## 2. 结果验证
### 2.1 渲染效果

(基于nerf天空模型) 实验1和实验2的对比视频如[链接1](https://github.com/user-attachments/assets/24ef8d46-4421-473d-9c23-78ee2e0d5e0f)；

(基于gs天空模型) 实验0和实验3的对比视频如[链接2](https://github.com/user-attachments/assets/47be620c-314f-4b26-8ddf-ee8c7df073d4)；

### 2.2 指标分析
通过 [FID](https://proceedings.neurips.cc/paper/2017/hash/8a1d694707eb0fefe65871369074926d-Abstract.html) 进行量化的指标计算，比较上述实验结果在Waymo测试集中的效果(目前测试1个场景，后续拓展)；

| Experiment   | Batch  |   DataSet |   Camera |    FID(↓) |
|:----------|----------:|------:|--------:|--------:|
| Exp0   |90000 |   Waymo049 |[0,1,2]    |    98.25| 
| Exp1   |90000 |   Waymo049 |[0,1,2]    |    78.67| 
| Exp2   |90000 |   Waymo049 |[0,1,2]    |    78.38| 
| Exp3   |90000 |   Waymo049 |[0,1,2]    |    **76.33**| 

---
对于实验3，我们额外分析了PSNR、SSIM在Interpolation实验(训练测试一半一半)中的表现并于baseline比较(未任何修复)。

| Experiment   | Batch  |   DataSet |   Camera |    PSNR(↑) |    SSIM(↑) |
|:----------|----------:|------:|--------:|--------:|--------:|
| Base   |30000 |   Waymo049 |[0]        |    31.51|     0.89|
| Exp3   |90000 |   Waymo049 |[0]        |    28.93|     0.85|
| Exp3   |90000 |   Waymo049 |[0,1,2]    |    27.75|     0.82| 

---

## 3. 总结 
> 1. 对于相机校正的图像渲染，可行的方案如下：   
> a. **第一次训练：训练集+nerf天空模型；b. 修复器修复获得修复集；c. 第二次训练：训练集+修复集+gs天空模型；**
> 2. 对于修复器，校正图像的长宽与原配置会有差别，需渲染新的点云图作为输入，注意该点云图中的椭球大小；
> 3. 对于修复样本，可以采取前m轮损失关注整张图像(天空+地面)，后n轮关注下半部分图像(地面)的训练方式；
