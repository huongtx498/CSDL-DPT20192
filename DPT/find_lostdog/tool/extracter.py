from find_lostdog.model.classify.eval import *
import mysql.connector
from mysql.connector import errorcode
from torchvision import transforms
import re
import pickle
import torch
from torchvision import models
import torch.nn as nn


class Extracter():
    def __init__(self, model_path, class_name_path):
        class_names = pickle.load(open('.\\class_names.pkl', 'rb'))
        _, self.extracter = load_model(
            'dog_classification_resnet.pth', class_names)

    def extract(self, img):
        '''
        img: Image 
        freatures size (1, 2048)
        '''
        features = extract(self.extracter, img).data
        features = features.view(2048)
        return features
