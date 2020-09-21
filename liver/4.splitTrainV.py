# 切图+制作数据集

import os
import shutil
import random
from PIL import Image
from PIL import ImageOps

# 滑窗切图
def processImg(srcDir, fn, tarDir, rows, cols):
    image = Image.open(f"{srcDir}/{fn}")
    # 反色
    image = ImageOps.invert(image)
    # 切图
    width, height = image.size
    item_width = 256
    item_height = 256
    # 保存每一个小切图的区域
    box_list = []
    for i in range(0, height - item_height + 1, (height - item_height) // (rows - 1)):
        for j in range(0, width - item_width + 1, (width - item_width) // (cols - 1)):
            # 切图区域是矩形，位置由对角线的两个点(左上和右下)确定
            box = (j, i, j + item_width, i + item_height)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    # 保存
    fns = []
    for (index, image) in enumerate(image_list):
        dn = f"{fn[:-4]}-{index}.png"
        image.save(f"{tarDir}/{dn}", "PNG")
        fns.append(dn)
    return fns

base_dir = 'D:/liver_data/try_train_vali_test/'
high = 'high_tmb'
low = 'low_tmb'
high_tiles = 'high_tmb_tiles'
low_tiles = 'low_tmb_tiles'
train_dir = base_dir +'/train'
test_dir = base_dir +'/test'
validation_dir = base_dir +'/validation'
if not os.path.exists(train_dir):
    os.mkdir(train_dir)
if not os.path.exists(test_dir):
    os.mkdir(test_dir)
if not os.path.exists(validation_dir):
    os.mkdir(validation_dir)
if not os.path.exists(train_dir + '/' + high):
    os.mkdir(train_dir + '/' + high)
if not os.path.exists(train_dir + '/' + low):
    os.mkdir(train_dir + '/' + low)
if not os.path.exists(test_dir + '/' + high):
    os.mkdir(test_dir + '/' + high)
if not os.path.exists(test_dir + '/' + low):
    os.mkdir(test_dir + '/' + low)
if not os.path.exists(validation_dir + '/' + high):
    os.mkdir(validation_dir + '/' + high)
if not os.path.exists(validation_dir + '/' + low):
    os.mkdir(validation_dir + '/' + low)
if not os.path.exists(train_dir + '/' + high_tiles):
    os.mkdir(train_dir + '/' + high_tiles)
if not os.path.exists(train_dir + '/' + low_tiles):
   os.mkdir(train_dir + '/' + low_tiles)
if not os.path.exists(test_dir + '/' + high_tiles):
    os.mkdir(test_dir + '/' + high_tiles)
if not os.path.exists(test_dir + '/' + low_tiles):
    os.mkdir(test_dir + '/' + low_tiles)
if not os.path.exists(validation_dir + '/' + high_tiles):
    os.mkdir(validation_dir + '/' + high_tiles)
if not os.path.exists(validation_dir + '/' + low_tiles):
    os.mkdir(validation_dir + '/' + low_tiles)


ratio = 0.2  # 验证集所占的比例

highfiles = os.listdir(base_dir + '/' + high)
highV = random.sample(highfiles, int(len(highfiles) * ratio))
for dn in highfiles:
    #if dn in highV:
        #shutil.move(f"{base_dir}/{high}/{dn}", f"{test_dir}/{high}/{dn}")
    if dn in highV:
        shutil.copytree(f"{base_dir}/{high}/{dn}", f"{validation_dir}/{high}/{dn}")
    else:
        shutil.copytree(f"{base_dir}/{high}/{dn}", f"{train_dir}/{high}/{dn}")


lowfiles = os.listdir(base_dir + '/' + low)
lowV = random.sample(lowfiles, int(len(lowfiles) * ratio))
for dn in lowfiles:
    #if dn in lowV:
        #shutil.move(f"{base_dir}/{low}/{dn}", f"{test_dir}/{low}/{dn}")
    if dn in lowV:
        shutil.copytree(f"{base_dir}/{low}/{dn}", f"{validation_dir}/{low}/{dn}")
    else:
        shutil.copytree(f"{base_dir}/{low}/{dn}", f"{train_dir}/{low}/{dn}")

'''
highFiles = []
highSrc = base_dir + '/' + high
for dn in os.listdir(highSrc):
    for fn in os.listdir(highSrc + '/' + dn):
    #if dn.find('TCGA-') == 0:
        fns = processImg(highSrc + '/' + dn, fn, train_dir + '/' + high, 4, 7)  # 8*15*371=44520
        highFiles += fns

lowFiles = []
lowSrc = base_dir + '/' + low
for dn in os.listdir(lowSrc):
    for fn in os.listdir(lowSrc + '/' + dn):
    #if dn.find('TCGA-') == 0:
        fns = processImg(lowSrc + '/' + dn, fn, train_dir + '/' + low, 4, 7)  # 4*7*1606=44968
        lowFiles += fns

# 划分验证集
#highFiles = os.listdir(train_dir + '/' + high)
highV = random.sample(highFiles, int(len(highFiles) * ratio))
for fn in highV:
    shutil.move(f"{train_dir}/{high}/{fn}", f"{validation_dir}/{high}/{fn}")

#lowFiles = os.listdir(train_dir + '/' + low)
lowV = random.sample(lowFiles, int(len(lowFiles) * ratio))
for fn in lowV:
    shutil.move(f"{train_dir}/{low}/{fn}", f"{validation_dir}/{low}/{fn}")
'''

# 20x cropped WSI --> 256*256 tiles
# cut out 256*256 tiles from local images(training set)
highSrc_train = train_dir + '/' + high
for dn in os.listdir(highSrc_train):
    if not os.path.exists(train_dir + '/' + high_tiles + '/' + dn):
        os.mkdir(train_dir + '/' + high_tiles + '/' + dn)
        for fn in os.listdir(highSrc_train + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(highSrc_train + '/' + dn, fn, train_dir + '/' + high_tiles, 12, 25)
lowSrc_train = train_dir + '/' + low
for dn in os.listdir(lowSrc_train):
    if not os.path.exists(train_dir + '/' + low_tiles + '/' + dn):
        os.mkdir(train_dir + '/' + low_tiles + '/' + dn)
        for fn in os.listdir(lowSrc_train + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(lowSrc_train + '/' + dn, fn, train_dir + '/' + low_tiles, 4, 7)

# cut out 256*256 tiles from local images(validation set)
highSrc_val = validation_dir + '/' + high
for dn in os.listdir(highSrc_val):
    if not os.path.exists(validation_dir + '/' + high_tiles + '/' + dn):
        os.mkdir(validation_dir + '/' + high_tiles + '/' + dn)
        for fn in os.listdir(highSrc_val + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(highSrc_val + '/' + dn, fn, validation_dir + '/' + high_tiles, 12, 25)
lowSrc_val = validation_dir + '/' + low
for dn in os.listdir(lowSrc_val):
    if not os.path.exists(validation_dir + '/' + low_tiles + '/' + dn):
        os.mkdir(validation_dir + '/' + low_tiles + '/' + dn)
        for fn in os.listdir(lowSrc_val + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(lowSrc_val + '/' + dn, fn, validation_dir + '/' + low_tiles, 4, 7)
'''

# cut out 256*256 tiles from local images(test set)
highSrc_test = test_dir + '/' + high
for dn in os.listdir(highSrc_test):
    if not os.path.exists(test_dir + '/' + high_tiles + '/' + dn):
        os.mkdir(test_dir + '/' + high_tiles + '/' + dn)
        for fn in os.listdir(highSrc_test + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(highSrc_test + '/' + dn, fn, test_dir + '/' + high_tiles + '/' + dn, 4, 7)
                
lowSrc_test = test_dir + '/' + low
for dn in os.listdir(lowSrc_test):
    if not os.path.exists(test_dir + '/' + low_tiles + '/' + dn):
        os.mkdir(test_dir + '/' + low_tiles + '/' + dn)
        for fn in os.listdir(lowSrc_test + '/' + dn):
            if fn.find('TCGA-') == 0:
                fns = processImg(lowSrc_test + '/' + dn, fn, test_dir + '/' + low_tiles + '/' + dn, 4, 7)
'''