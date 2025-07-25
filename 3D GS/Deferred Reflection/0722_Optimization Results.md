# 延迟反射优化记录报告
## 1.背景 
根据报告中的结论：本次实验主要将3DGS-DR中关于镜面反射图层的模块移植到了现有的框架中进行训练。结果是随着训练轮数增加环境图层逐渐退化为空白图，最终图像只受原始图层影响。针对其中提到的优化建议，我们设计了下述方案并进行验证。

方案包含了几个方面的考虑，
> 1. 统一3D-GS和DR的渲染器；
> 2. 对于动态物体，增加其损失权重；
> 3. 对于非动态物体，实验2种配置；a.其反射强度为0；b.其反射强度不为0，通过损失函数控制；
> 4. 最终成像，配置是否只在动态物体区域叠加反射光；

为了快速训练得到结果，实验数据为waymo_val_121场景中97-167帧的前置摄像头。

## 2.优化方案

| Experiment   |   Exp1 |
|:----------:|:------------:|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   refl_strength |  初始化：1e-3 对于动态物体，1e-6其它 |
|   最终成像 | `final_color = (1-refl_strength) * rendered_color[0] + refl_strength * refl_color`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound)` |
|   损失函数(反射) |   `loss += optim_args.lambda_reg * torch.where(obj_bound, -(ref_obj * torch.log(ref_obj) + (1. - ref_obj) * torch.log(1. - ref_obj)), -torch.log(1. - ref_obj)).mean()` |

| Experiment   |   Exp2 |
|:----------:|:-------------:|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   refl_strength |  初始化：1e-3 对于动态物体，1e-6其它 |
|   最终成像 | `final_color = rendered_color[0].clone() obj_bound = camera.guidance['obj_bound'].squeeze(0) if 'obj_bound' in camera.guidance else None final_color[obj_bound] = refl_color[obj_bound] * refl_strength[obj_bound] + rendered_color[0][obj_bound] * (1 - refl_strength[obj_bound])`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound) * 11` |
|   损失函数(反射) |   `_, refls_ndr = gaussians.get_refl if refls_ndr is not None and len(refls_ndr) > 0: refl_msk_loss = refls_ndr.mean() loss += REFL_MSK_LOSS_W * refl_msk_loss` |

| Experiment   |   Exp3 |
|:----------:|:-------------:|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   refl_strength |  初始化：1e-3 对于动态物体，1e-6其它；读取时动态物体原值，非动态物体0 |
|   最终成像 | `final_color = (1-refl_strength) * rendered_color[0] + refl_strength * refl_color`  |
|   损失函数(重建) |   `if gaussians.include_obj and obj_bound is not None and iteration < int(0.7 * training_args.iterations): ref_mask = render_pkg['refl_strength_map'] > 1e-4 if 'refl_strength_map' in render_pkg else None if ref_mask.sum() > 0: loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=ref_mask) ` |
|   损失函数(反射) |   --- |

## 3. 实验结果 

| Experiment   |   Batch |  PSNR_train(↑) | PSNR_test(↑) |   Envmap |
|:----------:|:-------------:|:----------:|:----------:|:----------:|
| No-DR  |   30000 | 27.36  | 26.67  |   --- |
| Exp1   |   30000 |  26.40 | 25.36  |  <img height="150" alt="image" src="https://github.com/user-attachments/assets/2823e1ba-f0e5-4e6f-9455-30f974354b8f" />|
| Exp2   |   30000 | 25.48  | 24.91  |  <img height="150" alt="image" src="https://github.com/user-attachments/assets/883551a1-4663-4cad-91aa-7a09c9f5ea4d" />|
| Exp3   |   30000 | 27.30  | 25.91  |  <img height="150" alt="image" src="https://github.com/user-attachments/assets/b210acaf-327d-4b52-ad2a-1f0764977537" />|

---

上述实验结果与预期偏差较大，待验证以反射光方向、反射位置为变量的环境贴图方案(模型/代码阻塞)。
