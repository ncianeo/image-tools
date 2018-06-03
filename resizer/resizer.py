from multiprocessing import Pool
import os
from PIL import Image

path = os.getcwd()
path = os.path.join(path,"original")

file_list = []
for root, dir, file in os.walk(path):
    for file_name in file:
        file_list.append(os.path.join(root,file_name))

for file_name in file_list:
    try:
        os.makedirs(os.path.dirname(file_name.replace("original","resized")))
    except:
        continue

def f(fp):
    if os.path.splitext(fp)[1].upper()==".JPG":
        print("processing %s" %(fp.replace('._','')))
        img = Image.open(fp.replace('._',''))
        icc_profile = img.info.get("icc_profile")
        width = img.size[0]
        height = img.size[1]
        if "big" in fp:
            newwidth = int(1000)
        elif "medium" in fp:
            newwidth = int(500)
        elif "layout" in fp:
            newwidth = int(1000)
        newheight = int(newwidth*height/width)
        img2 = img.resize((newwidth,newheight), Image.LANCZOS)
        img2.save(fp.replace('._','').replace("original","resized"), "JPEG", icc_profile = icc_profile)

if __name__ == '__main__':
    pool = Pool(6)
    pool.map(f, file_list)
