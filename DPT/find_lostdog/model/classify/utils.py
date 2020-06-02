import numpy as np
import matplotlib.pyplot as plt
import os
from shutil import copyfile


def train_test_split(data_dir):
    type_dirs = [os.path.join(data_dir, dir) for dir in os.listdir(data_dir) 
                    if os.path.isdir(os.path.join(data_dir, dir))]
    
    for type_dir in type_dirs:
        imgs = [os.path.join(type_dir, file) for file in os.listdir(type_dir) 
                    if os.path.isfile(os.path.join(type_dir, file))]
        num_img = len(imgs)
        train_imgs = imgs[:4*(num_img//5)]
        val_imgs = imgs[4*(num_img//5):num_img]

        cl = type_dir.split("\\")[-1]
        des_dir_train = '.\\dataset' + '\\train' + "\\" + cl
        os.makedirs(des_dir_train)
        for file in train_imgs:
            img_file = file.split("\\")[-1]
            des = des_dir_train + "\\" + img_file
            copyfile(file, des)
        
        des_dir_val = '.\\dataset' + '\\val' + "\\" + cl
        os.makedirs(des_dir_val)
        for file in val_imgs:
            img_file = file.split("\\")[-1]
            des = des_dir_val + "\\" + img_file
            copyfile(file, des)
        
    

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(20)


# train_test_split(".\\data\\Images")