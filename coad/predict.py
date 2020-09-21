from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
import os
import pandas as pd
import collections

def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    K.get_session().run(tf.local_variables_initializer())
    return auc

df = pd.DataFrame(pd.read_csv('TCGA-LIHC.muse_snv.tsv', sep='	'))

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
    c[k] /= 36
arr = list(zip(c.keys(), c.values()))
arr.sort(key = lambda x: x[1], reverse = True)

# 得到前32个病例
highTMB = set(e[0] for e in arr[:32])

# 开始预测
table = {
    '病例名': [],
    '图块数': [],
    '预测结果': [],
    '预测分类': [],
    '实际分类': [],
    '是否正确': [],
}
model = load_model('tcga_lihc_small_46.h5', {'auc': auc})
sample_dir = 'D:/liver_data/try/test/high_tmb/'
for dn in os.listdir(sample_dir):
    total = 0
    positive = 0
    for fn in os.listdir(sample_dir + dn):
        img_path = sample_dir + dn + '/' + fn
        img = image.load_img(img_path, target_size=(256, 256))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0) / 255.
        preds = model.predict(x)
        if preds[0][0] < 0.5:
            positive += 1
        total += 1
    result = positive / total
    table['病例名'].append(dn)
    table['图块数'].append(total)
    table['预测结果'].append(result)
    table['预测分类'].append('高' if result > 0.5 else '低')
    table['实际分类'].append('高' if dn in highTMB else '低')
    table['是否正确'].append('是' if table['预测分类'][-1] == table['实际分类'][-1] else '否')
    print(table['病例名'][-1], table['图块数'][-1], table['预测结果'][-1], table['预测分类'][-1], table['实际分类'][-1], table['是否正确'][-1])

dft = pd.DataFrame(table)
dft.to_csv('predict.csv', index=0)