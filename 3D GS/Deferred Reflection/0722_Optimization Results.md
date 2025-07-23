# 延迟反射优化记录报告
## 1.背景 
根据报告中的结论：本次实验主要将3DGS-DR中关于镜面反射图层的模块移植到了现有的框架中进行训练。结果是随着训练轮数增加环境图层逐渐退化为空白图，最终图像只受原始图层影响。针对其中提到的优化建议，我们设计了下述方案并进行验证。

为了快速训练得到结果，实验数据为waymo_val_121场景中97-167帧的前置摄像头。

## 2.优化方案

| Experiment   |   Exp1 |
|:----------:|:------------:|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   最终成像 | `final_color = (1-refl_strength) * rendered_color[0] + refl_strength * refl_color`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound)` |
|   损失函数(反射) |   `loss += optim_args.lambda_reg * torch.where(obj_bound, -(ref_obj * torch.log(ref_obj) + (1. - ref_obj) * torch.log(1. - ref_obj)), -torch.log(1. - ref_obj)).mean()` |

| Experiment   |   Exp2 |
|:----------:|:-------------:|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   最终成像 | `final_color = rendered_color[0].clone() obj_bound = camera.guidance['obj_bound'].squeeze(0) if 'obj_bound' in camera.guidance else None final_color[obj_bound] = refl_color[obj_bound] * refl_strength[obj_bound] + rendered_color[0][obj_bound] * (1 - refl_strength[obj_bound])`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound) * 2` |
|   损失函数(反射) |   `_, refls_ndr = gaussians.get_refl if refls_ndr is not None and len(refls_ndr) > 0: refl_msk_loss = refls_ndr.mean() loss += REFL_MSK_LOSS_W * refl_msk_loss` |

## 3. 实验结果 

| Experiment   |   Batch |  PSNR_train(↑) | PSNR_test(↑) |   Envmap |
|:----------:|:-------------:|:----------:|:----------:|:----------:|
| No-DR  |   30000 | 27.36 | 26.67  |   --- |
| Exp1   |   30000 |   |   |   |
| Exp2   |   30000 |   |   |   |
