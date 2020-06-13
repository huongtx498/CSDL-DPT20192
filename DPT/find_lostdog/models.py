# -*- coding: utf-8 -*-
from django.db import models
from .tool.CRUDdog import CRUD_Dog

modelpath = r'/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/dog_classification_resnet.pth'
classnamepath = r'/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/class_names.pkl'
user = 'admin'
pw = 'mmx1437cbcd'
url = 'localhost'
db_name = 'muti_media_db'

KV = [('Thanh Xuân', 'Thanh Xuân'), ('Hai Bà Trưng', 'Hai Bà Trưng'),
      ('Cầu Giấy', 'Cầu Giấy'), ('Ba Đình', 'Ba Đình'), ('Tây Hồ', 'Tây Hồ'), ]
PK = [('Không', 'Không'), ('Vòng cổ', 'Vòng cổ'),
      ('Xích', 'Xích'), ('Rọ mõm', 'Rọ mõm')]
TT = [('Khoẻ mạnh', 'Khoẻ mạnh'), ('Bị ốm', 'Bị ốm')]
MAU = [('Đen', 'Đen'), ('Nâu', 'Nâu'), ('Vàng', 'Vàng'),
       ('Đỏ', 'Đỏ'), ('Trắng', 'Trắng'), ('Cam', 'Cam')]

crud_dog = CRUD_Dog(modelpath, classnamepath)._get_all_type(
    user, pw, url, db_name)
dog_type = []
for dog in crud_dog:
    dog = dog.split("-", 1)[1]
    temp = (dog, dog)
    dog_type.append(temp)


class Image_db(models.Model):
    tag = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'create'


class Image_addPost(models.Model):
    dogImage = models.FileField(upload_to='addpost/')
    species = models.CharField(max_length=100, choices=dog_type)
    weight = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=100, choices=MAU)
    accessory = models.CharField(max_length=100, choices=PK)
    location = models.CharField(max_length=100, choices=KV)
    time = models.DateField()
    status = models.CharField(max_length=100, choices=TT)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'create'


class Image_searchPost(models.Model):
    dogImage = models.FileField(upload_to='searchpost/')
    species = models.CharField(max_length=100, choices=dog_type)
    weight = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=100, choices=MAU)
    accessory = models.CharField(max_length=100, choices=PK)
    location = models.CharField(max_length=100, choices=KV)
    time = models.DateField()
    status = models.CharField(max_length=100, choices=TT)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'create'
