# 点云预处理
将不同帧的点云拼接+动态物体去除，以便初始换静态背景。
## 1. 数据描述
GPS文件：100HZ，6000帧数据，通过week/second week确定时间戳，转换代码：

    def gps_week_seconds_to_utc(gpsweek, gpsseconds, leapseconds=LEAP_SECONDS):
      # 闰秒
      LEAP_SECONDS = 0
      datetimeformat = "%Y-%m-%d %H:%M:%S.%f"
      epoch = datetime.datetime.strptime("1980-01-06 00:00:00.000", datetimeformat)
      # timedelta函数会处理seconds为负数的情况
      elapsed = datetime.timedelta(days=(gpsweek*7), seconds=(gpsseconds-leapseconds))
      ori_time = datetime.datetime.strftime(epoch+elapsed, datetimeformat)
    return ori_time,int((epoch+elapsed).timestamp()),(epoch+elapsed).timestamp()

获得结果：
> 起始时间：'2024-09-13 01:28:53.440000', 1726190933, 1726190933.44   
> 结束时间：'2024-09-13 01:29:53.430000', 1726190993, 1726190993.43

点云文件：10HZ，596帧数据，直接给出时间戳，
> 起始时间：'2024-09-13 09:29:14', 1726190954.799706   
> 结束时间：'2024-09-13 09:30:14', 1726191014.200170

从时间戳上，两者差别21s。

## 2. 拼接结果
从轨迹时间戳上对齐，举例如下，其中绿色黄绿色为251帧点云，蓝绿色为351帧点云：
<div align=center>
<img src="https://github.com/user-attachments/assets/13f4d5e6-5e94-4d6b-a13a-609bf380e815" width="750px">
</div>

从轨迹顺序上对齐，举例如下，其中绿色黄绿色为251帧点云，蓝绿色为351帧点云：
<div align=center>
<img src="https://github.com/user-attachments/assets/92a73344-7483-48e9-bd2f-d6a847a13c96" width="750px">
</div>

> 根据上述数据观察，无论是轨迹时间戳对齐或者轨迹顺序对齐效果都较差，   
> 初步结论为**通过正常的方式利用GPS信息补齐点云数据较难实现**。

## 3. 强制拼接
> 将420帧点云和480帧点云强制拼接(轨迹顺序对齐，作为三维重建初始化，对精度要求没那么高)；   
> 上图为全部点云+点云检测结果；   
> 下图为压缩点云+去除目标物结果；   
<div align=center>
<img src="https://github.com/user-attachments/assets/1289908f-b9a4-4251-851d-92f6b5ad01aa" width="750px">
<img src="https://github.com/user-attachments/assets/556be3e0-f0a0-4210-9da3-2e98fd204a94" width="750px">
</div>

# 图像预处理
为了提升动静分离的效果，对原始图像进行掩码处理，加入第四通道(即是否mask)。

## 1. Pipeline
简要流程：
> 原始图像-目标检测-目标追踪-图像掩码；   
> 图像掩码的输入即目标追踪的输出，根据包围盒的8个顶点组成的凸多边形确定掩码形状；   
> 对于图像中包含的主车引擎盖，在v方向截断(取前1900帧)；

对于上述的截断操作，不影响相机的内参，其它参数无需改动。

## 2. 示例 
具体如下图所示，左边为截断后的图像，右边为掩码图像。
<div align=center>
<img src="https://github.com/user-attachments/assets/c631c8c1-b02a-4b04-a4a4-a58bec3a30af" width="488px">
<img src="https://github.com/user-attachments/assets/c1b3b0af-9e14-4bb1-a6b6-f431c167af64" width="500px">
</div>

# 参数预处理
构建训练过程中所使用参数信息，主要作用于坐标变换；
## 1. 数据格式
> 以json存储的dict数据；
> data："frames":*list(dict)*,"camera_angle_x":*float*；
> frames:"file_path","depth_path","transform_matrix","cx","cy","obj_rt","obj_quat"；

## 2. 示例 

{"frames": [{"file_path": "images/000000", "depth_path": "depth/000000.npy", "transform_matrix": [[-0.9619000184920027, 0.27301329534803115, 0.01456348132468067, 0.0], [-0.015238824419468396, -0.00035322877450637556, -0.9998838199809746, 0.0], [-0.2729764324175225, -0.9620101952643966, 0.004500172436718702, 0.0]], "cy": 1096.6, "cx": 1866.3, "obj_rt": [[[-0.00923166099176442, -0.015238824419468396, 0.9998412647343812, 6.560042856474543], [-0.9999572653108798, -0.00035322877450637556, -0.00923811568562362, 0.06685805362706367], [0.0004939507275429862, -0.9998838199809746, -0.015234912304745479, 23.064654077654904], [0.0, 0.0, 0.0, 1.0]], [[0.0, 0.0, 0.0, -9999.0], [0.0, 0.0, 0.0, -9999.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]], "obj_quat": [[0.49375606272960926, 0.5015866027137006, -0.5059924269497528, 0.4985854935368471], [0.0, 0.0, 0.0, 0.0]]}],"camera_angle_x": 1.5716717097190502}
