# CNN-predict-TMB
tsv文件用来计算TMB值(R script)
膀胱癌——BLCA	结肠癌——COAD	直肠癌——READ	肝癌——LIHC
四个文件夹分别为膀胱癌，结肠癌，肝癌和直肠癌代码，代码主体基本一致，仅文件读取。存储地址部分需要修改。其他内容可参考代码注释。
运行顺序为
1. filter：筛选病理图像，保证每个病例都有对应的基因数据可以计算TMB值
2. tmb_threshold：R script根据tsv文件的基因数据计算每个病例的TMB值，根据折线回归法选取TMB threshold
3. splitDataset: 根据上一步计算的threshold将所有病例分为高低TMB(label)，注意只选取20倍放大的病灶区切图数据
4. splitTrainV：将数据分为训练集、验证集和测试集
5. model_train_46：训练
6. predict：预测

1.5. get20x和4.5.splitTrainV_correct_local可省略， step1-4可在本地运行（需安装python和R），step5-6需在服务器运行（需配置相应环境 tensorflow/ker
