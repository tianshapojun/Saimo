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

- 使用Checkpoint：yolov10m.pt"；
- classes = [2,5,7]，其中各标签{2: 'car'5: 'bus'7: 'truck'}；

## 2.3 效果对比

以README中的两段视频为例，
- 视频1：未加入2D检测：追踪物体1791次；加入2D检测：追踪物体2053次；提升**14.63%**；
- 视频2：未加入2D检测：追踪物体239次；加入3D检测：追踪物体262次；提升**9.62%**；



### 2.3.1 边缘车辆

![00002](https://github.com/user-attachments/assets/694211c6-379c-404a-8b4c-a4dd8e500994)
![00023](https://github.com/user-attachments/assets/e2b388dc-38a5-413a-9427-e45a16a73866)
![00050](https://github.com/user-attachments/assets/4d78c30c-9728-4668-a8fe-76c2dac91709)
![00130](https://github.com/user-attachments/assets/6ed342da-9f86-42b7-beaa-2c28aa64a4c5)

### 2.3.2 缺帧补全 
![00056](https://github.com/user-attachments/assets/7cbbd5fc-fa1a-4686-85ca-e883b022485f)
![00232](https://github.com/user-attachments/assets/1bde02d5-1660-4ec0-9122-de99b13daf15)


