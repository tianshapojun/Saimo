# 不同场景中的车模移植 Part:1
对于训练好的一个场景模型，如仅使用场景内的动态车模进行泛化(主车、环境车控制)会有极大的局限性，在该场景内添加多种车辆类型、多种车辆外观是必要的。
因此，本topic讨论场景之间已训练好的动态物体模型移植的方案流程，期冀在存储一定量模型之后形成相应的模型库。

## 1. 整体方案
训练好的模型以.pth格式存储，stat_dict整体包含background、sky、objects三种key。因此，A场景调用b-object模型方案如下： 
> a. A场景setup_function加入b-object；   
> b. load_stat_dict中额外载入b-object信息；   
> c. parse_camera的function中更改b-object轨迹；   
> d. 更新球协函数中的观察角度；

对于点d，模拟光照颜色的球协基函数的输入之一为观测角度的方向(极坐标的 $\theta$ 和 $\varphi$ )，具体公式如下

$$
f(\theta,\varphi) = \sum_{l=0}^{\infty} \sum_{m=-l}^l C_l^m Y_l^m(\theta,\varphi),
$$

其中 $Y_l^m$ 即为球谐基函数， $C_l^m $为学习的系数。而观测角度是世界坐标系下的。举例说明，同样是在主车视角观察前车，两个场景下场景A的观察方向为(1，0，0),
场景B的观察方向为(-1，0，0)，从而导致颜色的不同(见下图，其中左图为A场景(原始场景)中仅渲染车辆a的效果，右图为车辆B场景(移植场景)中仅渲染车辆a的效果，观测角度影响球谐基函数，
从而影响渲染颜色)。

---

<table rules="none" align="center">
  <tr>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/efbf6c89-3c58-4951-82b3-fb943647007b" height="200px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;原始场景中仅渲染车辆a.png</font>
      </center>
    </td>
    <td> 
      <center>
        <img src="https://github.com/user-attachments/assets/2f0bc2ef-11ff-498c-b471-bd4cad69e1e1" height="200px">
        <br/>
        <font color="AAAAAA">&emsp;&emsp;&emsp;移植场景中仅渲染车辆a.png</font>
      </center>
    </td>
  </tr>
</table>

---

## 2.移植效果
移植效果的图像如下： 

<div align=center>
<img src="https://github.com/user-attachments/assets/fb33d4a5-7291-45da-9ff6-2d3b7569d347" width="650px">
</div>

---

移植效果的视频如[链接](https://github.com/user-attachments/assets/96bd50d6-0b83-4e15-a549-8d324a53c0b2)。

## 3.问题和总结
通过演示视频，移植效果初步满足需求，未完成及可改进的内容如下： 
> a. object模型拆分保存；   
> b. object航向角控制；   
> c. 移植object嵌入新background的高拟真度；
