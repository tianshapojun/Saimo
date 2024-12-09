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
