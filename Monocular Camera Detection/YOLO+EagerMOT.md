# 1. 总体流程

通过YOLO10的2D检测结果+MONODETR的3D检测结果输入到追踪算法EagerMOT中，提升追踪效果。

# 2. 技术细节

## 2.1 EagerMOT的2D感知输入
以官方推荐的 TrackRCNN detections/segmentations 结果进行数据分析，下边为其中一样例，

0 1109.5554 179.36575 1197.3547 314.45007 0.9999083 2 375 1242 Ygf<5b;0000O2...

- 第 1 列：帧号，生效；
- 第 2-5 列：bbox 坐标，生效；
- 第 6 列：检测置信度，生效；
- 第 7 列：物体类别 (1 为 car，2 为行人)，生效；
- 第 8-9 列：图像 (h,w)，未生效；
- 第 10 列：掩码 (RLE，Run-length encoding 格式，参考 COCO 表达方式)，未生效；
- 第 11 列：未显示，ReID(re-identification ID)，物体的特征向量，在原文中进行追踪，未生效；

## 2.2 YOLO配置

YOLOv10("yolov10m.pt")
classes = [2,5,7]
2: 'car'
5: 'bus'
7: 'truck'
