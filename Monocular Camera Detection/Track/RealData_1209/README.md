# 1. 数据描述
主车信息：(世界坐标系)坐标，航向角；   
环境车信息：(世界坐标系)坐标，航向角；   
帧率：1HZ；   
帧数：824帧；

# 2. 追踪算法参数配置
max_ages=(5, 3),   
min_hits=(1, 2),   
det_scores=(0.0, 0),   
seg_scores=(0.0, 0.9),   
fusion_iou_threshold=(0.01, 0.01),   
first_matching_method="dist_2d_full",   
thresholds_per_class={1: -50, 2: -0.3  }, # car, ped   
max_age_2d=(3, 3),   
leftover_matching_thres=0.3,   
compensate_ego=True;   

# 3. 追踪效果
具体的追踪效果可见1204_fill/1204_unfill.mp4视频(主车为原点，车头方向为x轴，车辆右侧为y轴)，后者有补帧操作；   
追踪效果一般，分析下来存在的原因包括：   
> **帧率较低，帧与帧之间变动较大(车辆位置、车辆数量)；**   
> **数据较脏，例如530帧左右，环境车快速贴近主车又快速远离主车；**