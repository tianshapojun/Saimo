import numpy as np
import cv2
import math
from PIL import Image,ImageFont,ImageDraw
import glob 
import os
from tqdm import tqdm

def img_magic(fig_loc,folder): 
    #I_ori = np.array([[1252.8131021185304, 0.0, 826.588114781398], [0.0, 1252.8131021185304, 469.9846626224581], [0.0, 0.0, 1.0]])
    I_ori = np.array([[1266.417203046554, 0.0, 816.2670197447984], [0.0, 1266.417203046554, 491.50706579294757], [0.0, 0.0, 1.0]])
    #I_dest = np.array([[7.215377000000e+02,0.000000000000e+00,6.095593000000e+02],[0.000000000000e+00,7.215377000000e+02,1.728540000000e+02],[0.000000000000e+00,0.000000000000e+00,1.000000000000e+00]])
    I_dest = np.array( [[2081.6967190566124, 0.0,  9.6e+02], [0.0, 2081.6967190566124, 6.4e+02], [0.0, 0.0, 1.0]])

    img = cv2.imread(fig_loc)
    height_ori,width_ori = img.shape[0], img.shape[1]
    height_dest,width_dest = 1280,1920

    img_new = np.zeros((height_dest,width_dest,3))
    # simp
    map_x = np.zeros((height_dest, width_dest), dtype=np.float32)
    map_y = np.zeros((height_dest, width_dest), dtype=np.float32)

    for i in range(height_dest): 
        for j in range(width_dest): 
            u1 = (j - I_dest[0,2])/I_dest[0,0] * I_ori[0,0] + I_ori[0,2]
            v1 = 1.495 / 2.116 * (i - I_dest[1,2])/I_dest[1,1] * I_ori[1,1] + I_ori[1,2]
            map_x[i, j] = u1
            map_y[i, j] = v1

            # if u1>=1 and u1<= width_ori-2 and v1>=1 and v1<= height_ori-2:
            #     #img_new[i,j,:] = img[int(v1),int(u1),:]
            #     img_new[i,j,:] = (1-v1+int(v1))*((1-u1+int(u1))*img[int(v1),int(u1),:] + (u1-int(u1))*img[int(v1),math.ceil(u1),:]) +\
            #     (v1-int(v1))*((1-u1+int(u1))*img[math.ceil(v1),int(u1),:] + (u1-int(u1))*img[math.ceil(v1),math.ceil(u1),:])
    
    img_new = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    fig_name = (fig_loc.split("/"))[-1]
    cv2.imwrite('./data/nuscenes_try/{}/{}'.format(folder,fig_name),img_new)
    
    # o_w, o_h = int(I_ori[0,2]), int(I_ori[1,2])
    # img_new = img[int(o_h-height_dest/2):int(o_h+height_dest/2),int(o_w-width_dest/2):int(o_w+width_dest/2),:]
    # cv2.imwrite('./t2.png',img_new)
    
    # img_new = cv2.resize(img,(width_dest,height_dest),interpolation=cv2.INTER_NEAREST)
    # cv2.imwrite('./t3.png',img_new)

def concate_img(image_paths):
    #images = [Image.open(image_path+'/%05d.png'%(index)) if idx > 0 else\
              #Image.open(image_path+'/%06d.png'%(index)) for idx,image_path in enumerate(image_paths)]
    images = [Image.open(image_path) for image_path in image_paths]

    # 2. 获取图片尺寸
    image_sizes = [image.size for image in images]

    #target_size = (int(image_sizes[0][0]/image_sizes[0][1]*image_sizes[1][1]),image_sizes[1][1])
    target_size = (image_sizes[1][0],int(image_sizes[0][1]/image_sizes[0][0]*image_sizes[1][0]))
    images[0] = images[0].resize(target_size)
    image_sizes[0] = target_size

    # 3. 计算长图尺寸
    long_image_width = max([size[0] for size in image_sizes])
    long_image_height = sum([size[1] for size in image_sizes])

    # 4. 创建空白长图
    long_image = Image.new('RGB', (long_image_width, long_image_height))

    # 5. 拼接图片
    y_offset = 0
    title_list = ['Origin','Cropped','Resized','Projected']
    font = ImageFont.truetype('/usr/share/fonts/type1/urw-base35/C059-Roman.t1',size=24)
    for idx,image in enumerate(images):
        title = title_list[idx]
        draw = ImageDraw.Draw(image)
        draw.text((int(long_image_width/2),10),title,font =font,fill='black')
        long_image.paste(image, (0, y_offset))
        y_offset += image.size[1]

    # 6. 保存长图
    long_image.save('./t_all.png')

if __name__=="__main__":
     
    for folder in ['curved']: 
        fig_locs = sorted(glob.glob(os.path.join('/root/Codes/tracking/EagerMOT/data/nuscenes/figure/{}'.format(folder) , '*.jpg')))
        for fig_loc in tqdm(fig_locs): 
            img_magic(fig_loc,folder)

    # 1. 加载图片
    # image_paths = [
    #             fig_name,
    #             './t2.png',
    #             './t3.png',
    #             './t1.png',
    #             ]
    # concate_img(image_paths)
