import os
import shutil
import random

base_dir = 'D:/liver_data'
high = 'high_tmb'
low = 'low_tmb'
train_dir = 'D:/liver_data/train'
validation_dir = 'D:/liver_data/validation'

radio = 0.2  # 验证集所占的比例

highTiles = {}
lowTiles = {}

for fn in os.listdir(train_dir + '/' + high):
    sample = fn[:fn.rfind('-')]
    if not highTiles.__contains__(sample):
        highTiles[sample] = []
    highTiles[sample].append(fn)

for fn in os.listdir(train_dir + '/' + low):
    sample = fn[:fn.rfind('-')]
    if not lowTiles.__contains__(sample):
        lowTiles[sample] = []
    lowTiles[sample].append(fn)

for fn in os.listdir(validation_dir + '/' + high):
    shutil.move(f"{validation_dir}/{high}/{fn}", f"{train_dir}/{high}/{fn}")
    sample = fn[:fn.rfind('-')]
    if not highTiles.__contains__(sample):
        highTiles[sample] = []
    highTiles[sample].append(fn)

for fn in os.listdir(validation_dir + '/' + low):
    shutil.move(f"{validation_dir}/{low}/{fn}", f"{train_dir}/{low}/{fn}")
    sample = fn[:fn.rfind('-')]
    if not lowTiles.__contains__(sample):
        lowTiles[sample] = []
    lowTiles[sample].append(fn)

# 随机划分局部图片1000次，取训练数据最接近的一次
bestHighTK = []
bestLowTK = []
htk = highTiles.keys()
ltk = lowTiles.keys()
minTmp = 10000
for i in range(1000):
    highTK = random.sample(htk, int(len(htk) * (1-radio)))
    lowTK = random.sample(ltk, int(len(ltk) * (1-radio)))
    highTC = sum(len(highTiles[k]) for k in highTK)
    lowTC = sum(len(lowTiles[k]) for k in lowTK)
    if abs(highTC - lowTC) < minTmp:
        minTmp = abs(highTC - lowTC)
        bestHighTK = highTK
        bestLowTK = lowTK
        print(minTmp, highTC, lowTC)

highV = []
for k in htk - bestHighTK:
    highV += highTiles[k]

lowV = []
for k in ltk - bestLowTK:
    lowV += lowTiles[k]

# 划分验证集
for fn in highV:
    shutil.move(f"{train_dir}/{high}/{fn}", f"{validation_dir}/{high}/{fn}")

for fn in lowV:
    shutil.move(f"{train_dir}/{low}/{fn}", f"{validation_dir}/{low}/{fn}")
                    
