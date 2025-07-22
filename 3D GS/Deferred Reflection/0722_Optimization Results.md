# 延迟反射优化记录报告
## 1.背景 

## 2.优化方案

| Experiment   |   EXP1 |
|:----------|:-------------|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   最终成像 | `final_color = (1-refl_strength) * rendered_color[0] + refl_strength * refl_color`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound)` |
|   损失函数(反射) |   `loss += optim_args.lambda_reg * torch.where(obj_bound, -(ref_obj * torch.log(ref_obj) + (1. - ref_obj) * torch.log(1. - ref_obj)), -torch.log(1. - ref_obj)).mean()` |

| Experiment   |   EXP1 |
|:----------|:-------------|
|   渲染器(3D-GS) | gsplat  |
|   渲染器(DR) |  gsplat |
|   最终成像 | `final_color = rendered_color[0].clone() obj_bound = camera.guidance['obj_bound'].squeeze(0) if 'obj_bound' in camera.guidance else None final_color[obj_bound] = refl_color[obj_bound] * refl_strength[obj_bound] + rendered_color[0][obj_bound] * (1 - refl_strength[obj_bound])`  |
|   损失函数(重建) |   `loss += optim_args.lambda_l1 * l1_loss(image, gt_image, mask=obj_bound)` |
|   损失函数(反射) |   `_, refls_ndr = gaussians.get_refl if refls_ndr is not None and len(refls_ndr) > 0: refl_msk_loss = refls_ndr.mean() loss += REFL_MSK_LOSS_W * refl_msk_loss` |

