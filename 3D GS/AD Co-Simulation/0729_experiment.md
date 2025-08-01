# 0729 AD联仿感知模块评估

# 1. 实验设置和结果
实验中三维重建模块与[UniAD](https://arxiv.org/abs/2212.10156)联仿，评估其感知模块并与YOLO10进行比较，相关的实验设置和结果如下图所示。

<div align=center>
<img src="https://github.com/user-attachments/assets/57ad0ca1-4398-4f54-8bd2-e3d552dec6b8" width="1000px">
</div>


| Scene   | # Frames  |   TP |   FP |    FN |    Recall(↑) |   OTA_IoU(↑) | Other |
|:----------|:----------|:------|:--------|:--------|:--------|:--------|:--------|
| 121   | 48 |   105 |  425   |  22 | 0.827 | 0.648 | 以左右平移修复
| 049   | 18 |   30  |  137   |  29 | 0.508 | 0.451 | 以nuscenes配置为修复
| 002   | 20 |   61  |  10    |  2  | 0.968 | 0.785 | 以左右平移修复

** 049场景相关指标较低的原因包括GT车辆被前车遮挡、举例较远、分辨率较低；   
** YOLO感知算法的相关指标符合预期；

---


# 2. 相关视频
汇总了GT值和YOLO感知结果，其中YOLO行框上的数字代表***置信度***；Matched行框上的数字代表***IoU***，绿色框表示匹配上的GT框，红色框表示未匹配上的GT框；

## 2.1 Waymo_121 

https://github.com/user-attachments/assets/de99b99a-a083-43ae-a694-513f6ad3fa7f

## 2.2 Waymo_049

https://github.com/user-attachments/assets/3a2c3a6f-1349-489d-930d-f9d4527b04ba

## 2.3 Waymo_049

https://github.com/user-attachments/assets/6ff34dd2-4a5e-489e-bd2e-0e7b2a798efe








