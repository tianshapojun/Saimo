# 1. 数据描述
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

# 2. 拼接结果
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

# 3. 强制拼接
> 将420帧点云和480帧点云强制拼接(轨迹顺序对齐，作为三维重建初始化，对精度要求没那么高)；   
> 上图为全部点云+点云检测结果；   
> 下图为压缩点云+去除目标物结果；   
<div align=center>
<img src="https://github.com/user-attachments/assets/1289908f-b9a4-4251-851d-92f6b5ad01aa" width="750px">
<img src="https://github.com/user-attachments/assets/556be3e0-f0a0-4210-9da3-2e98fd204a94" width="750px">
</div>


