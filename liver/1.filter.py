# 将TMB数据中的病例与图像数据比对，删除有图像但无基因数据的病例，重命名图像数据

import os
import shutil
import pandas as pd

proj = 'LIHC'
originalDir = 'D:/liver_data/cropped_TCGA'
newDir = 'D:/liver_data/try_all_tiles/filtered'

path = 'C:/Users/Skyvein/Desktop/TMB/通用流程/通用流程' #path of tsv file
df = pd.DataFrame(pd.read_csv(path + '/TCGA-' + proj + '.muse_snv.tsv', sep='	'))
samples = set(df['Sample_ID'])
if not os.path.exists(newDir):
    os.mkdir(newDir)

#index = 0
data = os.listdir(originalDir)
for dn in data:
    for dn2 in os.listdir(originalDir + '/' + dn):
        if dn2.find('TCGA-') == 0:
            sample = dn2[:16]
            if sample in samples:
                shutil.copytree(originalDir + '/' + dn, newDir + '/' + dn2[:23])
                #shutil.move(newDir + '/' + dn2[:23], newDir + '/' + sample) #rename folders
            break
    #index += 1
    #print(index, '/', len(data))