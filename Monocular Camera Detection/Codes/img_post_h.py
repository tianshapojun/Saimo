from PIL import Image
import os 
from tqdm import tqdm

def concate_img(index,image_paths):
    #images = [Image.open(image_path+'/%05d.png'%(index)) if idx > 0 else\
              #Image.open(image_path+'/%06d.png'%(index)) for idx,image_path in enumerate(image_paths)]
    images = [Image.open(image_path+'/%05d.png'%(index)) for image_path in image_paths]

    # 2. 获取图片尺寸
    image_sizes = [image.size for image in images]

    #target_size = (int(image_sizes[0][0]/image_sizes[0][1]*image_sizes[1][1]),image_sizes[1][1])
    target_size = (image_sizes[0][0],int(image_sizes[1][1]/image_sizes[1][0]*image_sizes[0][0]))
    images[1] = images[1].resize(target_size)
    image_sizes[1] = target_size

    # 3. 计算长图尺寸
    long_image_width = max([size[0] for size in image_sizes])
    long_image_height = sum([size[1] for size in image_sizes])

    # 4. 创建空白长图
    long_image = Image.new('RGB', (long_image_width, long_image_height))

    # 5. 拼接图片
    y_offset = 0
    for image in images:
        long_image.paste(image, (0,y_offset))
        y_offset += image.size[1]

    # 6. 保存长图
    long_image.save('/root/Codes/tracking/EagerMOT/figures/1119_nj/concat_1204/%05d.png'%(index))

if __name__ == "__main__":
    # 1. 加载图片
    image_paths = [
                #'/root/Codes/tracking/EagerMOT/figures/0904_ens/straight/FOV_try_topo2d',
                #'/root/Codes/tracking/EagerMOT/figures/0904_ens/straight/BEV_try_topo2d'
                '/root/Codes/tracking/EagerMOT/figures/1119_nj/FOV_try_topo2d',
                '/root/Codes/tracking/EagerMOT/figures/1119_nj/BEV_try_topo2d'
                ]
    n_files = len(os.listdir(image_paths[0]))
    
    for i in tqdm(range(n_files)): 
        concate_img(i, image_paths)
