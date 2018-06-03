import os
import io
import numpy as np
import imageio
from multiprocessing import Pool
from PIL import Image
from PIL import ImageCms

img_sizes = {'big':1000, 'medium':700, 'tiny':700, 'small':700}

srgb = ImageCms.createProfile('sRGB')

target_path = 'target images'
gif_path = 'gif images'

item_list = [dir for dir in os.listdir(target_path) if os.path.isdir(os.path.join(target_path,dir))]

def read(item):
    print('reading %s...' %item)
    item_path = os.path.join(target_path,item)
    srcs = []
    if not os.path.isdir(item_path):
        os.makedirs(item_path)
    for file in os.listdir(item_path):
        if file.split('.')[-1].upper() in ['JPG', 'JPEG', 'PNG']:
            img = Image.open(os.path.join(item_path,file))
            icc_profile = img.info.get('icc_profile')
            f = io.BytesIO(icc_profile)
            try:
                icc=ImageCms.ImageCmsProfile(f)
                img = ImageCms.profileToProfile(img,icc,srgb)
            except:
                pass
            srcs.append(np.asarray(img))
    return item, srcs

def make(itemsrcs):
    item = itemsrcs[0]
    srcs = itemsrcs[1]
    if item_gifsrc[item]!=[]:
        try:
            if not os.path.isdir(gif_path):
                os.makedirs(gif_path)
            print('saving %s.gif' %item)
            imageio.mimwrite(os.path.join(gif_path,item+'.gif'), srcs, duration=1)
        except:
            print('ERROR: An error occured! Target images might have different sizes or this is an IO error.')

def read_and_make(item):
    print('reading %s...' %item)
    item_path = os.path.join(target_path,item)
    srcs = []
    if not os.path.isdir(item_path):
        os.makedirs(item_path)
    for file in os.listdir(item_path):
        if file.split('.')[-1].upper() in ['JPG', 'JPEG', 'PNG']:
            img = Image.open(os.path.join(item_path,file))
            icc_profile = img.info.get('icc_profile')
            f = io.BytesIO(icc_profile)
            try:
                icc=ImageCms.ImageCmsProfile(f)
                img = ImageCms.profileToProfile(img,icc,srgb)
            except:
                pass
            srcs.append(np.asarray(img))
    if srcs!=[]:
        try:
            if not os.path.isdir(gif_path):
                os.makedirs(gif_path)
            print('saving %s.gif' %item)
            imageio.mimwrite(os.path.join(gif_path,item+'.gif'), srcs, duration=1)
        except:
            print('ERROR: An error occured! Target images might have different sizes or this is an IO error.')
            
            
if __name__=="__main__":           
    pool = Pool(8)
    pool.map(read_and_make,item_list)
