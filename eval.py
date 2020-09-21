#https://blog.csdn.net/u014380165/article/details/78634829
#https://https://github.com/miraclewkf/ImageClassification-PyTorch/blob/master~\\/level2/train\_customData.py
from __future__ import print_function, division
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torch.autograd import Variable
from torchvision import  models, transforms

import time
import os
from torch.utils.data import Dataset

from PIL import Image

# use PIL Image to read image
def default_loader(path):
    try:
        img = Image.open(path)
        return img.convert('RGB')
    except:
        print("Cannot read image: {}".format(path))


# define your Dataset. Assume each line in your .txt file is [name/tab/label], for example:0001.jpg 1
# txt文件中每行都是图像路径，tab键，标签
# 定义数据读取接口
class customData(Dataset):
    def __init__(self, img_path, txt_path, dataset = '', data_transforms=None, loader = default_loader):
        with open(txt_path) as input_file:
            lines = input_file.readlines()
            self.img_name = [os.path.join(img_path, line.strip().split('\t')[0]) for line in lines]
            self.img_label = [int(line.strip().split('\t')[-1]) for line in lines]
        self.data_transforms = data_transforms
        self.dataset = dataset
        self.loader = loader

    def __len__(self):
        return len(self.img_name)

    def __getitem__(self, item):
        img_name = self.img_name[item]
        label = self.img_label[item]
        img = self.loader(img_name)

        if self.data_transforms is not None:
            try:
                img = self.data_transforms[self.dataset](img)
            except:
                print("Cannot transform image: {}".format(img_name))
        return img, label

# load the exist model
model = torch.load("output/best_resnet.pkl")

if __name__ == '__main__':
#  Transform中将每张图像都封装成Tensor
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    use_gpu = torch.cuda.is_available()

    batch_size = 42
    num_class = 2

# 调用数据读取接口
    image_datasets = {x: customData(img_path='./picture',
                                    txt_path=('./txt/' + x + '.txt'),
                                    data_transforms=data_transforms,
                                    dataset=x) for x in ['val']}
    print(len(image_datasets))

# 将这个batch的图像数据和标签都分别封装成Tensor
    # wrap your data and label into Tensor
    dataloders = {x: torch.utils.data.DataLoader(image_datasets[x],
                                                 batch_size=batch_size,
                                                 shuffle=True) for x in ['val']}

#    dataset_sizes = {x: len(image_datasets[x]) for x in ['val']}

# define cost function
criterion = nn.CrossEntropyLoss()
# criterion = nn.MultiLabelSoftMarginLoss()

#model eval
model.eval()
eval_loss = 0.0
eval_acc = 0.0
for data in dataloders['val']:
    img,label = data
#    img = img.view(img.size(0), -1)
#    img = Variable(img.cuda())
    img = Variable(img)
    # img = img.type(torch.FloatTensor)
    # label = Variable(label.cuda())
    label = Variable(label)
    out = model(img)
    loss = criterion(out, label)
    eval_loss += loss.data[0] * label.size(0)
    _,pred = torch.max(out, 1)
    num_correct = (pred == label).sum()
    # eval_acc = eval_acc.float()
    eval_acc += num_correct.data[0]

    # out = model(img)
    # loss = criterion(out, label)
    # running_loss += loss.data[0] * label.size(0)
    # _, pred = torch.max(out, 1)
    # num_correct = (pred == label).sum()
    # running_acc += num_correct.data[0]
    # 向后传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


    # print(data)
    print(pred)
    print('Test Loss: {:.6f}, Acc: {:.6f}'.format(eval_loss / (len(pred)),eval_acc / (len(pred))))
    print( num_correct)
    # print( _,pred )
    print(len(pred))
    print(eval_loss / (len(pred)))
    print(eval_acc / (len(pred)))
    print(eval_acc)
    print(eval_loss)
    # print(out)