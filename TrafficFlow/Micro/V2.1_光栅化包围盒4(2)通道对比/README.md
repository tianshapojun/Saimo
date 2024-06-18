# 0. 总结
在cd_light./test/多种车道类型.xodr三张地图上进行测试，

# 1. 模型训练相关配置
为简化表达，4通道模型记为M1，2通道模型几位M2，除通道数外，两者的差别为：

M1：v = 输入速度 * 255 / 120

M2：v = 255 - 输入速度 * 255 * 3.6 / 120

两者选取相同epoch=27，训练相关指标如下：

M1：Epoch 27, MAE: 0.03, RMSE: 0.07, MAPE: 7.6809%；

M2：Epoch 27, MAE: 0.04, RMSE: 0.07, MAPE: 8.1874%；

# 2. 相关效果比较
## 2.1 测试地图：cd_light.xodr

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/0ef8e2f3-6ae6-4f53-81a0-67f157095e30" width="500px">
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/79af7cf3-70ef-4212-8878-eeb28ab5f17b" width="500px">

## 2.2 测试地图：多种车道类型.xodr

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/c1cb941b-0f7c-449d-838d-d3e837da445b" width="500px">
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/08d6d526-a53f-447f-80af-a51e7b613843" width="500px">

## 2.3 测试地图：test.xodr

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/550f017a-daa9-4cea-8205-c88602b28934" width="500px">
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/6898031b-eaa6-4fca-a88b-1055013f48e9" width="500px">
