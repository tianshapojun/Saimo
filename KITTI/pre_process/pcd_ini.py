# 3D GS点云初始化准备文件
# 包含点云数据(pcd.bin)和配置相关文件(transforms_train.json)
import numpy as np
import json
import os
import cv2
import pickle
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from tqdm import tqdm

from utils.imu_utils import load_pointsclouds,Calibration_W2C,compress_pcd
from utils.camera_utils import Calibration,inverse_rigid_trans

def get_lidar_in_image_fov(
    pc_velo, calib, xmin, ymin, xmax, ymax, return_more=False, clip_distance=1.0
):
    """ Filter lidar points, keep those in image FOV """
    #pts_2d = calib.project_velo_to_image(pc_velo)
    pts_2d = calib.project_velo_to_image_new(pc_velo)
    fov_inds = (
        (pts_2d[:, 0] < xmax-1)
        & (pts_2d[:, 0] >= xmin)
        & (pts_2d[:, 1] < ymax-1)
        & (pts_2d[:, 1] >= ymin)
    )
    fov_inds = fov_inds & (pc_velo[:, 0] > clip_distance)
    imgfov_pc_velo = pc_velo[fov_inds, :]
    if return_more:
        return imgfov_pc_velo, pts_2d, fov_inds
    else:
        return imgfov_pc_velo

def pcds_render(root_dir, folder, idx_list, idx_list_2, compress = False):
    calib_filename = os.path.join(root_dir,'Data',folder,'calib','{}.txt'.format(folder))
    calib = Calibration(calib_filename, from_origin=False)
    pcd,poses = load_pointsclouds(root_dir, calib, folder, idx_list)
    print(pcd.shape)
    print(pcd[:,0].min(),pcd[:,0].max(),pcd[:,1].min(),pcd[:,1].max(),pcd[:,2].min(),pcd[:,2].max())
    print(pcd[:,3].min(),pcd[:,3].max())
    # save 
    #save_dir = os.path.join(root_dir,'output','pcd.bin')
    #pcd.astype(np.float32).tofile(save_dir)
    #quit()
    if compress:
        pcd = compress_pcd(pcd)[:,:3]
    else:
        pcd = pcd[:,:3]
    pcd_c = np.concatenate((pcd[:,:3],np.zeros((pcd.shape[0],4))), axis = 1)
    pcd_c[:,6] = np.infty

    transforms_train = {}
    transforms_train['frames'] = []
    
    for i,idx in enumerate(tqdm(idx_list_2)):
        img_filename = os.path.join(root_dir,'Data',folder,'image_2', '{}.png'.format("%06d" % (idx)))
        img = cv2.imread(img_filename)
        img_height, img_width, _ = img.shape
        
        n = pcd.shape[0]
        pcd_hom = np.hstack((pcd, np.ones((n, 1))))
        pcd_imu = np.dot(pcd_hom, np.transpose(inverse_rigid_trans(poses[i][:3,:4])))
        pcd_hom = np.hstack((pcd_imu, np.ones((n, 1))))
        pcd_v = np.dot(pcd_hom, np.transpose(calib.I2V))
        imgfov_pc_rect = calib.project_velo_to_rect(pcd_v)
        depth = imgfov_pc_rect[:, 2]
        imgfov_pc_velo, pts_2d, fov_inds = get_lidar_in_image_fov(
            pcd_v, calib, 0, 0, img_width, img_height, True
        )
        fov_inds = fov_inds & (pcd_c[:,6] > depth)
        
        imgfov_pts_2d = pts_2d[fov_inds, :]
        imgfov_pts_2d = np.round(imgfov_pts_2d).astype(np.int32)
        color_pcd = img[imgfov_pts_2d[:,1],imgfov_pts_2d[:,0]]        
        pcd_c[fov_inds, 3:6] = color_pcd
        pcd_c[fov_inds, 6] = depth[fov_inds]

        # transforms_train['frames]
        calib_c = Calibration_W2C(calib, poses[i][:3,:4], img_height, img_width)
        file_path = 'images/{}'.format("%06d" % (idx))
        transforms_train['frames'].append({'file_path':file_path, 'transform_matrix':calib_c.W2C.tolist(), 'cy':calib_c.cy, 'cx':calib_c.cx})
        
        # calib_c = Calibration2_W2C(calib, poses[i][:3,:4], img_height, img_width)
        # file_path = 'images/{}'.format("%010d" % (idx))
        # transforms_train['frames'].append({'file_path':file_path, 'transform_matrix':calib_c.W2C.tolist(), 'cy':calib_c.cy, 'cx':calib_c.cx})
        
    transforms_train['camera_angle_x'] = 2*np.arctan(img_width/(2*calib.P_new[0,0]))    
    
    print(pcd_c.shape)
    pcd_c = pcd_c[pcd_c[:,6] != np.infty]
    print(pcd_c.shape)
    
    # check folder
    save_folder = os.path.join(root_dir,'output',folder)
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    # save pcd
    save_dir = os.path.join(root_dir,'output',folder,'pcd.bin')
    pcd_c[:,:6].astype(np.float32).tofile(save_dir)
    # save json
    with open(os.path.join(root_dir,'output',folder,'transforms_train.json'), "w") as f:
        json.dump(transforms_train, f)

if __name__=="__main__":
    idx = 0
    folder = 'train_05'
    root_dir = os.path.dirname(os.path.abspath(__file__))

    pcds_render(root_dir, folder,[idx+i for i in range(0,100,20)],[idx+i for i in range(0,100,1)])
