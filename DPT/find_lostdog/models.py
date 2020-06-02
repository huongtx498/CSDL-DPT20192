# -*- coding: utf-8 -*-
from django.db import models


class Image_db(models.Model):
    tag = models.CharField(max_length=50)
    image = models.FileField(upload_to='images/')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'create'
