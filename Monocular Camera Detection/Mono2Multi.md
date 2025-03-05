# 1. 单目流程概述
整体流程如下，主要包含单目感知-多目标追踪-追踪轨迹优化三个模块。

<div align=center>
  <img src="https://github.com/user-attachments/assets/5b6006e6-5327-4e2b-b64b-6ed6f38334e2" width="500px">
</div>

# 2. 多目感知/端到端模块替换Pipeline 
* 对于多目感知，单帧输入为环视图像而非单目图像(前置摄像头)，需要将感知模块进行替换；输出内容与单目感知基本一致；
* 对于端到端感知(即感知追踪一体化)，追踪模块亦被替代，结构改变较大；

具体情况如下图所示：

<div align=center>
  <img src="https://github.com/user-attachments/assets/fe82fcdc-375b-4054-b305-3f64efc3b965" width="400px">
  <img src="https://github.com/user-attachments/assets/c8766f75-d705-4d06-b648-c756d18cf947" width="400px">
</div>


