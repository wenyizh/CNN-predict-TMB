# 对每个病例进行查询，把高tmb和低tmb的20x局部癌灶图像分开

import os
import shutil
import pandas as pd
import collections

base_dir = 'D:/liver_data/try_train_vali_test/dataset_5_8'
high_dir = base_dir + '/high_tmb'
low_dir = base_dir + '/low_tmb'
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
if not os.path.exists(high_dir):
    os.mkdir(high_dir)
if not os.path.exists(low_dir):
    os.mkdir(low_dir)

tsv_dir = 'C:/Users/Skyvein/Desktop/TMB/通用流程/通用流程'
df = pd.DataFrame(pd.read_csv(tsv_dir + '/TCGA-LIHC.muse_snv.tsv', sep='	'))

qt_dir = 'D:/liver_data/try_train_vali_test/filtered'


# 筛选出有害突变
samples = []
sampleDic = dict()
for i in range(len(df['Sample_ID'])):
    if df['filter'][i] == 'PASS' and ('coding_sequence_variant' in df['effect'][i]
    or 'frameshift_variant' in df['effect'][i]
    or 'inframe_' in df['effect'][i]
    or 'missense_variant' in df['effect'][i]
    or 'splice_' in df['effect'][i]
    or 'start_' in df['effect'][i]
    or 'stop_' in df['effect'][i]):
        samples.append(df['Sample_ID'][i])
        if not sampleDic.__contains__(df['Sample_ID'][i]):
            sampleDic[df['Sample_ID'][i]] = len(sampleDic)

# 对突变数目计数
c = dict(collections.Counter(samples))
for k in c.keys():
    c[k] /= 36 # 36 is a constant, means 36 megabytes
arr = list(zip(c.keys(), c.values()))
arr.sort(key = lambda x: x[1], reverse = True)


# 得到前#个病例
highTMB = set(e[0] for e in arr[:32]) # the number of high TMB cases are calculated from R script
lowTMB = set(e[0] for e in arr[32:64])

# 统计切过的切片
for dn in os.listdir(qt_dir):
    if dn.find('TCGA-') == 0:
        sample = dn[:16]
        if sampleDic.__contains__(sample) and dn.find('-bad') < 0:
            slices = os.listdir(qt_dir + '/' + dn)
            for dn2 in slices:
                if dn2[-3:] == 'tif' and dn2.find('-20X') >= 0:
                    src = qt_dir + '/' + dn + '/' + dn2
                    if sample in highTMB:
                        if not os.path.exists(high_dir + '/' + sample):
                            os.mkdir(high_dir + '/' + sample)
                        shutil.copyfile(src, high_dir + '/' + sample + '/' +  dn2)
                    elif sample in lowTMB:
                        if not os.path.exists(low_dir + '/' + sample):
                            os.mkdir(low_dir + '/' + sample)
                        shutil.copyfile(src, low_dir + '/' + sample + '/' +  dn2)
                    
