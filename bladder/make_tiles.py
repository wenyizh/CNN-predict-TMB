# make tiles(256 by 256)

import os
import shutil
from PIL import Image
from PIL import ImageOps


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


originalDir = 'D:/bladder_data/FGFR3M'
newDir = 'D:/bladder_data/test'
#testDir = 'D:/bladder_data/test'

if not os.path.exists(newDir):
    os.mkdir(newDir)

for dn in os.listdir(originalDir):
    #print(dn[:16])
    if not os.path.exists(newDir + '/' + dn[:16]):
        os.mkdir(newDir + '/' + dn[:16])
    for fn in os.listdir(originalDir + '/' + dn):
        if fn[-3:] == 'tif' and fn.find('-20x') >= 0:
            processImg(originalDir + '/' + dn, fn, newDir + '/' + dn[:16], 4, 7)
            #shutil.copyfile(originalDir + '/' + dn + '/' + fn,  newDir + '/' + dn + '/' + fn)
