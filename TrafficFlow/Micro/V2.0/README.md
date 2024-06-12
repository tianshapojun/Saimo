# 1. 版本优化
<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/b5e46deb-4515-4847-9d87-793936ea60b3" width="750px">
</div>

前处理修改部分：
1. 光栅化包围盒，增加两通道(中心为车辆中心，长宽为1，颜色=速度*255/120)；
2. 光栅化地图，为了对应主车非0航向角，参数设置更新为：\
    "raster_size_pre": [256,256], \
    "raster_size_post": [128,64], #\
    "pixel_size_pre": [0.5,0.5], \
    "pixel_size_post": [0.5,0.5], #\
    "ego_center_pre": [0.5,0.5], \
    "ego_center_post": [0.25,0.5], #\
3. 光栅化地图，增加停止线/当前车道中心线(独占1通道，待讨论是否需要加入下一条车道中心线)；
4. 矢量化特征部分：增加速度、航向角、车辆类型；

# 2. 效果展示
地图：cd_light.xodr，无后处理效果；

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/be344970-3047-40ae-9699-13bde264b819" width="500px">
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/4968bc60-31dd-4d9a-a320-44c485e7f36d" width="500px">

相关细节：
训练阶段：预测未来30帧(1s)的数据；

推理阶段：预测未来10帧的数据；

# 3. 存在的问题

## 3.1 在直道和一定曲率弯道的交接处，无法及时转向；
地图：cd_loop.xodr
<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/99399a54-ecb4-472c-ad53-90fc459f379f" width="600px">
</div>

## 3.2 在弯道冲出车道
地图: test.xodr,

<img src="https://github.com/tianshapojun/Saimo/assets/10208337/23851b6f-8511-408e-8492-f679fa0a5e74" width="500px">
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/f0c3d8e4-f1c3-4142-8378-9f0abf3037f7" width="500px">

验证发现，仅改变车道中心线颜色，发车点位置、速度、车型一致的情况下，冲出车道的情况消失，预估与训练数据(地图)相关；因为训练数据中，弯道95%以上为白线；

<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/53baf731-1363-4496-ba89-f8e94caf5248" width="600px">
</div>

## 3.3 不同速度样本不足

<div align=center>
<img src="https://github.com/tianshapojun/Saimo/assets/10208337/41d64fe4-26a8-4343-a9ce-c5f21f0e5b08" width="400px">
</div>

## 3.4 交叉口接口问题，训练中

## 3.5 待测问题：拥堵、交通灯控制；
