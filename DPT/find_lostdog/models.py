# -*- coding: utf-8 -*-
from django.db import models


class Image_db(models.Model):
    tag = models.CharField(max_length=50)
    image = models.FileField(upload_to='images/')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'create'


class Image_addPost(models.Model):
    dogImage = models.FileField(upload_to='addpost/')
    species = models.CharField(max_length=100)
    weight = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=100)
    accessory = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.DateField(max_length=100)
    status = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'create'


class Image_searchPost(models.Model):
    dogImage = models.FileField(upload_to='searchpost/')
    species = models.CharField(max_length=100)
    weight = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=100)
    accessory = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.DateField(max_length=100)
    status = models.CharField(max_length=100)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'create'
