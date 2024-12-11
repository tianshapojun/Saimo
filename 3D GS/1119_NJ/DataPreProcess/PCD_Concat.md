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

从时间戳上，两者差别21s，
