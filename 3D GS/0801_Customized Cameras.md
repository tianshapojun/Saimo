# 自定义相机推导流程记录

在给定训练相机的相关参数后，增加一定数量的额外相机以提升模型的功能性，提升生成数据的泛化性。在此，我们着重研究如何快速给出额外增加相机的相关参数及其背后的数学原理。

## 1. 内参/外参/图像长宽

对于内参/图像长宽，可以直接沿用训练相机的数据，而对于额外增加的相机一般是其外参做出变化。

训练数据的内参一般通过旋转矩阵表示，而最简单直接调整相机的外参是调整其航向角(欧拉角之一)，相关原理于下界给出。

## 2. [旋转矩阵->欧拉角，欧拉角->旋转矩阵](https://zhuanlan.zhihu.com/p/652238256)
## 2.1 欧拉角
在直角坐标系中，假设X是前方，Y是左方，Z是上方，那么绕X轴旋转是roll，绕Y轴旋是pitch，绕Z轴得到的是yaw。

对于右手系，用右手的大拇指指向旋转轴正方向，其他4个手指在握拳过程中的指向便是旋转的正方向。一般，roll、pitch和yaw的范围均定义在(-pi，+pi)。

于x,y,z三个轴的不同旋转顺序一共有(x-y-z, y-z-x, z-x-y, x-z-y, z-y-x, y-x-z)六种组合，在旋转角度相同的情况下不同的旋转顺序得到的姿态是不一样的。

> 欧拉角的外旋：每次旋转是绕固定轴（一个固定参考系，比如世界坐标系）的旋转。   
> 欧拉角的内旋：每次旋转是绕自身旋转之后的轴的旋转。

内旋中，Z-Y-X旋转顺序(指先绕自身轴Z，再绕自身轴Y，最后绕自身轴X)，可得旋转矩阵(内旋是右乘):

$$
R = R_z(\phi) R_y(\theta) R_x(\psi)
$$

外旋中，X-Y-Z旋转顺序(指先绕固定轴X，再绕固定轴Y，最后绕固定轴Z)，可得旋转矩阵(外旋是左乘)，表达式与上述一致。这个结论说明***Z-Y-X顺序的内旋等价于X-Y-Z顺序的外旋***。

## 2.2 旋转矩阵

<div align=left>
<img src="https://github.com/user-attachments/assets/8ef69531-1f5c-4b81-8ca8-596a37c685ae" height="350px"/>
<img src="https://github.com/user-attachments/assets/d2830a7e-21aa-4db3-bf03-5e21c907fc0d" height="250px"/>
</div>

## 2.3 相关代码
旋转拒转→欧拉角
```python
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

def rotationMatrixToEulerAngles(R) :
    assert(isRotationMatrix(R))
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
    return np.array([x, y, z])
```

欧拉角→旋转矩阵
```python
def euler_to_rotMat(yaw, pitch, roll):
    Rz_yaw = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [          0,            0, 1]])
    Ry_pitch = np.array([
        [ np.cos(pitch), 0, np.sin(pitch)],
        [             0, 1,             0],
        [-np.sin(pitch), 0, np.cos(pitch)]])
    Rx_roll = np.array([
        [1,            0,             0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]])
    rotMat = np.dot(Rz_yaw, np.dot(Ry_pitch, Rx_roll))
    return rotMat
```

## 2.4 实例分析及相关设计
以Waymo/Nuscenes的前置三个摄像头举例，其欧拉角分别如下(前3为nuscenes，后3为waymo)：

> Euler angles: theta_x: -1.5764, theta_y: -0.0008, theta_z: -1.5651   
> Euler angles: theta_x: -1.5683, theta_y: 0.0021, theta_z: -0.6081   
> Euler angles: theta_x: -1.5844, theta_y: 0.0091, theta_z: -2.5552   
> Euler angles: theta_x: -1.5815, theta_y: -0.0049, theta_z: -1.5805   
> Euler angles: theta_>x: -1.5881, theta_y: -0.0103, theta_z: -0.8003   
> Euler angles: theta_x: -1.5880, theta_y: -0.0036, theta_z: -2.3475

其主要差别为theta_z,即航向角。由此，设计如下方案：

对于新增的N个摄像头，第i个摄像头外参的欧拉角为
> theta_x: **-pi/2**,   
> theta_y: **0**,   
> theta_z: **zmin + i * (zmax - zmin) / (N + 1)**

其中zmax = max{theta_z ∈ train cameras}，zmax = min{theta_z ∈ train cameras}，注意 $arctan2 \in (-pi, pi]$。
