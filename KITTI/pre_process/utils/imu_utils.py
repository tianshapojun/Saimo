import numpy as np
import os
from .camera_utils import Calibration,inverse_rigid_trans
#import mayavi.mlab as mlab
from tqdm import tqdm
import pandas as pd

er = 6378137. # average earth radius at the equator

def latlonToMercator(lat,lon,scale):
    ''' converts lat/lon coordinates to mercator coordinates using mercator scale '''

    mx = scale * lon * np.pi * er / 180
    my = scale * er * np.log( np.tan((90+lat) * np.pi / 360) )
    return mx,my

def latToScale(lat):
    ''' compute mercator scale from latitude '''
    scale = np.cos(lat * np.pi / 180.0)
    return scale

def convertOxtsToPose(oxts):
    ''' converts a list of oxts measurements into metric poses,
    starting at (0,0,0) meters, OXTS coordinates are defined as
    x = forward, y = right, z = down (see OXTS RT3000 user manual)
    afterwards, pose{i} contains the transformation which takes a
    3D point in the i'th frame and projects it into the oxts
    coordinates with the origin at a lake in Karlsruhe. '''
    
    # origin in OXTS coordinate
    origin_oxts = [48.9843445, 8.4295857] # lake in Karlsruhe
    #origin_oxts = oxts[0,:2]
    
    # compute scale from lat value of the origin
    scale = latToScale(origin_oxts[0])
    
    # origin in Mercator coordinate
    ox,oy = latlonToMercator(origin_oxts[0],origin_oxts[1],scale)
    origin = np.array([ox, oy, 0])
    ox,oy = latlonToMercator(oxts[0,0],oxts[0,1],scale)
    origin = np.array([ox, oy, oxts[0,2]])
    
    pose = []
    
    # for all oxts packets do
    for i in range(len(oxts)):
        
        # if there is no data => no pose
        if not len(oxts[i]):
            pose.append([])
            continue
    
        # translation vector
        tx, ty = latlonToMercator(oxts[i,0],oxts[i,1],scale)
        t = np.array([tx, ty, oxts[i,2]])
    
        # rotation matrix (OXTS RT3000 user manual, page 71/92)
        rx = oxts[i,3] # roll
        ry = oxts[i,4] # pitch
        rz = oxts[i,5] # heading 
        Rx = np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]]) # base => nav  (level oxts => rotated oxts)
        Ry = np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]]) # base => nav  (level oxts => rotated oxts)
        Rz = np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]]) # base => nav  (level oxts => rotated oxts)
        R  = np.matmul(np.matmul(Rz, Ry), Rx)
        
        # normalize translation
        t = t-origin
            
        # add pose
        pose.append(np.vstack((np.hstack((R,t.reshape(3,1))),np.array([0,0,0,1]))))
    
    return pose

def postprocessPoses (poses_in):

    R = np.array([[1,0,0,0], [0,-1,0,0], [0,0,-1,0], [0,0,0,1]])
    
    poses  = []
    
    for i in range(len(poses_in)):
        P = poses_in[i]
        poses.append( np.matmul(R, P.T).T )
    
    return poses

def read_pointcloud(root_dir, folder, file_index, calib, pose):
    pointcloud = np.fromfile(os.path.join(root_dir,'Data', folder,'velodyne','{}.bin'.format(file_index)), dtype=np.float32, count=-1).reshape([-1, 4])
    pointcloud = pointcloud[:,:3]
    n = pointcloud.shape[0]
    pcd_hom = np.hstack((pointcloud, np.ones((n, 1))))
    pcd_imu = np.dot(pcd_hom, np.transpose(calib.V2I))
    pcd_hom = np.hstack((pcd_imu, np.ones((n, 1))))
    pcd_fin = np.dot(pcd_hom, np.transpose(pose))
    pcd_fin = np.concatenate((pcd_fin, int(file_index[-3:])*np.ones((n, 1))),axis=1)
    return pcd_fin

def load_pointsclouds(root_dir, calib, folder, idxs):
    file_index_1 = "%06d" % (idxs[0])
    
    oxts_dir = os.path.join(root_dir,'Data',folder,'oxts','{}.txt'.format(folder))
    oxts = np.loadtxt(oxts_dir)
    poses = convertOxtsToPose(oxts)
    # convert coordinate system from
    #   x=forward, y=right, z=down 
    # to
    #   x=forward, y=left, z=up
    # poses = postprocessPoses(poses)
    
    pcd_concate= read_pointcloud(root_dir, folder,file_index_1, calib, poses[idxs[0]][:3,:4])
    for i in range(1,len(idxs)): 
        file_index_2 = "%06d" % (idxs[i])
        pcd_2 = read_pointcloud(root_dir, folder, file_index_2, calib, poses[idxs[i]][:3,:4])
        pcd_concate = np.concatenate((pcd_concate, pcd_2), axis=0)
    
    return pcd_concate,poses

class cal_simple(object):
    def __init__(self,R,T):
        I2V = np.zeros((3,4))
        I2V[:3,:3] = np.array(R).reshape(3,3)
        I2V[:3,3] = np.array(T)
        self.V2I = inverse_rigid_trans(I2V)

def load_pointsclouds_new(root_dir, calib, folder, idxs, poses_only = False):
    file_index_1 = "%010d" % (idxs[0])
    
    #R = [9.999976e-01,7.553071e-04,-2.035826e-03,-7.854027e-04,9.998898e-01,-1.482298e-02,2.024406e-03,1.482454e-02,9.998881e-01]
    #T = [-8.086759e-01,3.195559e-01,-7.997231e-01]
    #calib = cal_simple(R,T)
    
    oxts = np.zeros((len(idxs),30))
    for i,idx in enumerate(idxs):
        oxts_dir = os.path.join(root_dir,'Data',folder,'oxts','data','{}.txt'.format("%010d" % (idx)))
        oxt = np.loadtxt(oxts_dir)
        oxts[i] = oxt 

    poses = convertOxtsToPose(oxts)
    if poses_only: 
        return poses
    # convert coordinate system from
    #   x=forward, y=right, z=down 
    # to
    #   x=forward, y=left, z=up
    # poses = postprocessPoses(poses)
    
    pcd_concate= read_pointcloud(root_dir, folder, file_index_1, calib, poses[0][:3,:4])
    for i in tqdm(range(1,len(idxs))): 
        file_index_2 = "%010d" % (idxs[i])
        pcd_2 = read_pointcloud(root_dir, folder, file_index_2, calib, poses[i][:3,:4])
        pcd_concate = np.concatenate((pcd_concate, pcd_2), axis=0)
    
    return pcd_concate, poses

def compress_pcd(pcd , voxel_size = [0.15, 0.15, 0.15]): 
    x = pcd[:, 0]  # x position of point
    y = pcd[:, 1]  # y position of point
    z = pcd[:, 2]  # z position of point
    xmax, xmin, ymax, ymin, zmax, zmin = x.max(),x.min(),y.max(),y.min(),z.max(),z.min()

    pcd_new = np.concatenate((pcd, np.zeros((pcd.shape[0],3))), axis = 1)
    pcd_new[:,4] = np.round((pcd_new[:,0]-xmin)/voxel_size[0]).astype(np.int32)
    pcd_new[:,5] = np.round((pcd_new[:,1]-ymin)/voxel_size[1]).astype(np.int32)
    pcd_new[:,6] = np.round((pcd_new[:,2]-zmin)/voxel_size[2]).astype(np.int32)
    pcd_df = pd.DataFrame(pcd_new, columns = ['x','y','z','id','xbin','ybin','zbin'])
    pcd_df_gp = pcd_df.groupby(['xbin','ybin','zbin']).agg({'x':'median','y':'median','z':['median','count']})
    pcd_df_gp = np.array(pcd_df_gp)
    pcd_df_gp = pcd_df_gp[pcd_df_gp[:,3]>5]
    
    return pcd_df_gp
        
class Calibration_W2C(object):
    def __init__(self, calib, pose, height, width):
        self.I2W = pose
        self.W2I = inverse_rigid_trans(pose)
        self.I2V = calib.I2V
        self.V2C = calib.V2C_new
        self.Instr = calib.P_new
        self.cx = calib.P_new[0,2]
        self.cy = calib.P_new[1,2]
        self.fx = calib.P_new[0,0]
        self.fy = calib.P_new[1,1]
        
        W2I_hom = np.vstack((self.W2I, np.array([[0,0,0,1]])))
        I2V_hom = np.vstack((self.I2V, np.array([[0,0,0,1]])))
        V2C_hom = np.vstack((self.V2C, np.array([[0,0,0,1]])))
        self.W2C = np.dot(V2C_hom, np.dot(I2V_hom, W2I_hom))[:3,:4]
        self.C2W = inverse_rigid_trans(self.W2C)
        self.W2V = np.dot(I2V_hom, W2I_hom)[:3,:4]   
        
        fovx = 2*np.arctan(width/(2*self.Instr[0,0]))
        fovy = 2*np.arctan(height/(2*self.Instr[1,1]))   
        
    def cart2hom(self, pts_3d):
        """ Input: nx3 points in Cartesian
            Oupput: nx4 points in Homogeneous by pending 1
        """
        n = pts_3d.shape[0]
        pts_3d_hom = np.hstack((pts_3d, np.ones((n, 1))))
        return pts_3d_hom
    
    def w2v(self, pcd): 
        pts_3d_velo = self.cart2hom(pcd)  # nx4
        return np.dot(pts_3d_velo, np.transpose(self.W2V))
    
    def v2c(self, pcd): 
        pts_3d_velo = self.cart2hom(pcd)  # nx4
        return np.dot(pts_3d_velo, np.transpose(self.V2C))
    
    def p2w(self,pcd_ini):
        pcd =pcd_ini.copy() 
        pcd[:,0] *= pcd[:,2]
        pcd[:,1] *= pcd[:,2]
        pcd[:,0] = (pcd[:,0]-pcd[:,2]*self.Instr[0,2])/self.Instr[0,0]
        pcd[:,1] = (pcd[:,1]-pcd[:,2]*self.Instr[1,2])/self.Instr[1,1]
        pts_3d_velo = self.cart2hom(pcd)  # nx4
        return np.dot(pts_3d_velo, np.transpose(self.C2W))
        
class Calibration2_W2C(object):
    def __init__(self, calib, pose, height, width):
        self.I2W = pose
        self.W2I = inverse_rigid_trans(pose)
        self.I2V = calib.I2V
        self.V2C = calib.V2C2_new
        self.Instr = calib.P2_new
        self.cx = calib.P2_new[0,2]
        self.cy = calib.P2_new[1,2]
        self.fx = calib.P2_new[0,0]
        self.fy = calib.P2_new[1,1]
        
        W2I_hom = np.vstack((self.W2I, np.array([[0,0,0,1]])))
        I2V_hom = np.vstack((self.I2V, np.array([[0,0,0,1]])))
        V2C_hom = np.vstack((self.V2C, np.array([[0,0,0,1]])))
        self.W2C = np.dot(V2C_hom, np.dot(I2V_hom, W2I_hom))[:3,:4]  
        
        fovx = 2*np.arctan(width/(2*self.Instr[0,0]))
        fovy = 2*np.arctan(height/(2*self.Instr[1,1]))  
        
    
             
    
