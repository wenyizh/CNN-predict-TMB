#fetch 20x cropped images
import os
import shutil

path1 = 'D:/liver_data/filtered/' #all filtered-cropped images are stored in this path
path2 = 'D:/liver_data/20x/'  #20x cropped images are stored in this path
if not os.path.exists(path2):
    os.mkdir(path2)

#index = 0
for dn in os.listdir(path1):
    for fn in os.listdir(path1 + dn):
        if fn.find('-20X') >= 0: #get 20x images
                                 # fn.find(): if exists, return index, else return -1
            if not os.path.exists(path2 + dn):
                os.mkdir(path2 + dn)
            shutil.copy(path1 +  dn + '/' + fn, path2 + dn) # copy 20x cropped images from orig path to new path
    #index += 1
    #print(index, '/', len(os.listdir(path1)))