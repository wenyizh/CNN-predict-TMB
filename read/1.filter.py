# 将TMB数据中的病例与图像数据比对，删除有图像但无基因数据的病例，重命名图像数据

import os
import shutil
import pandas as pd

proj = 'READ'
originalDir = 'D:/read/cropped_TCGA'
newDir = 'D:/read/filtered'

path = 'C:/Users/Skyvein/Desktop/TMB/code' #path of tsv file
df = pd.DataFrame(pd.read_csv(path + '/TCGA-' + proj + '.muse_snv.tsv', sep='	'))
samples = set(df['Sample_ID'])
if not os.path.exists(newDir):
    os.mkdir(newDir)

#index = 0
data = os.listdir(originalDir)
for dn in data:
    #for dn2 in os.listdir(originalDir + '/' + dn):
        #if dn2.find('TCGA-') == 0:
        sample = dn[:16]
        if sample in samples:
            shutil.copytree(originalDir + '/' + dn, newDir + '/' + dn)
                #shutil.move(newDir + '/' + dn2[:23], newDir + '/' + sample) #rename folders
            #break
    #index += 1
    #print(index, '/', len(data))