import io
import os
import random
import datetime
import matplotlib.image as mpimg
import mysql.connector
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from mysql.connector import errorcode
from .forms import *
from django.http import HttpResponse
from PIL import Image
from pathlib import Path
from .forms import *
from .models import *
from find_lostdog.tool.findDogType import FindDogType
from find_lostdog.FP.main import FindPost
from find_lostdog.tool.CRUDdog import CRUD_Dog
from find_lostdog.FP.CRUDpost import CRUD_Post


class Post():
    def __init__(self, spiece, weights, heights, colors, access, area, time, status, type):
        self.spiece = spiece
        self.weights = weights
        self.heights = heights
        self.colors = colors
        self.access = access
        self.area = area
        self.time = time
        self.status = status
        self.type = type

# Create your views here.


modelpath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/dog_classification_resnet.pth'
classnamepath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/class_names.pkl'
user = 'admin'
pw = 'mmx1437cbcd'
url = 'localhost'
db_name = 'muti_media_db'

# Search dog from tag and image


def getImageByName(dog_type):
    folder = "media/Images/"+dog_type
    images = []
    img1 = random.choice(os.listdir(folder))
    img1_url = "media/Images/"+dog_type+"/"+img1
    img2 = random.choice(os.listdir(folder))
    img2_url = "media/Images/"+dog_type+"/"+img2
    images.append(img1_url)
    images.append(img2_url)
    print(images)
    return images


def searchDog(request):
    dog = {}
    list_dogtype = []
    if request.method == 'POST':
        dogForm = SearchDogForm(request.POST or None, request.FILES or None)
        if dogForm.is_valid():
            dogForm.save()

        # Lay url anh
        Dogs = Image_db.objects.latest()
        dogPath = ("." + str(Dogs.image.url))
        path = Path(dogPath).resolve()

        # Khoi tao cac doi tuong control
        compare = FindDogType(modelpath, classnamepath, user, pw, url, db_name)
        crud_dog = CRUD_Dog(modelpath, classnamepath)
        crud_post = CRUD_Post()

        # Chuyen anh sang dang binary
        image_bytes = crud_post.convertToBinaryData(path)
        image = Image.open(io.BytesIO(image_bytes))

        # Thuc hien va tra ket qua so sanh
        # results = compare._find_dog_type_from_tag(Dogs.tag)
        # results = compare._find_dog_type_from_img(image)
        results = compare.find_dog_type(image, str(Dogs.tag))
        for result in results:
            dog.info = crud_dog._getDogByType(
                user, pw, url, db_name, result)  # Thong tin ket qua loai cho
            dogimage = getImageByName(result)  # Mang 2 hinh anh ket qua
            list_dogtype.append(dog)   # Dict cua cac loai cho tra ve
        print(path)
        print(results)
        return render(request, 'find_lostdog/searchDog.html', {'listdogs': list_dogtype, 'image_url': path, 'form': dogForm})
    else:
        dogForm = SearchDogForm()
        return render(request, 'find_lostdog/searchDog.html', {'form': dogForm})


# Add new post to find dog


def addPost(request):
    submitbutton = request.POST.get("submit")
    image = ''
    image0 = ''
    spiece = ''
    colors = ''
    access = ''
    area = ''
    time = ''
    status = ''
    weights = 0
    heights = 0
    type = 0  # post bai dang
    image_url = ''

    if request.method == 'POST':
        addForm = PostForm(request.POST, request.FILES)
        if addForm.is_valid():

            # Lay url anh
            image0 = request.FILES['dogImage']
            fs = FileSystemStorage()
            filename = fs.save(image0.name, image0)
            image_url = fs.url(filename)

            # Thong tin khac
            spiece = addForm.cleaned_data.get('species')
            weights = addForm.cleaned_data.get('weight')
            heights = addForm.cleaned_data.get('height')
            colors = addForm.cleaned_data.get('color')
            access = addForm.cleaned_data.get('accessory')
            area = addForm.cleaned_data.get('location')
            time = addForm.cleaned_data.get('time')
            status = addForm.cleaned_data.get('status')

            # Duong dan tuyet doi cua anh
            img_url = ("." + str(image_url))
            imagePath = Path(img_url).resolve()

            # Tao doi tuong post
            post = Post(spiece, weights, heights, colors,
                        access, area, time, status, type)
            crud_addpost = CRUD_Post()

            # Them post vao csdl Post
            crud_addpost._add_post(user, pw, url, db_name, post, imagePath)
            print(post.spiece+" "+str(post.weights)+" " +
                  str(post.heights)+" "+str(post.time))
            print(imagePath)
            return render(request, 'find_lostdog/post.html', {'image_url': imagePath, 'post': post, 'form': addForm})

    else:
        addForm = PostForm()
        return render(request, 'find_lostdog/post.html', {'form': addForm})


def searchLostDog(request):
    submitbutton = request.POST.get("submit")
    image = ''
    image0 = ''
    spiece = ''
    colors = ''
    access = ''
    area = ''
    time = ''
    status = ''
    weights = 0
    heights = 0
    type = 1  # post tim kiem
    image_url = ''

    if request.method == 'POST':
        searchLostDogForm = SearchLostDogForm(request.POST, request.FILES)
        if searchLostDogForm.is_valid():

            # Lay url anh
            image0 = request.FILES['dogImage']
            fs = FileSystemStorage()
            filename = fs.save(image0.name, image0)
            image_url = fs.url(filename)

            # Lay cac thong tin khac
            spiece = searchLostDogForm.cleaned_data.get('species')
            weights = searchLostDogForm.cleaned_data.get('weight')
            heights = searchLostDogForm.cleaned_data.get('height')
            colors = searchLostDogForm.cleaned_data.get('color')
            access = searchLostDogForm.cleaned_data.get('accessory')
            area = searchLostDogForm.cleaned_data.get('location')
            time = searchLostDogForm.cleaned_data.get('time')
            status = searchLostDogForm.cleaned_data.get('status')

            # Duong dan tuyet doi cua anh
            img_url = ("." + str(image_url))
            imagePath = Path(img_url).resolve()

            # Tao doi tuong searchPost
            searchPost = Post(spiece, weights, heights, colors,
                              access, area, time, status, type)
            crud_addpost = CRUD_Post()

            # Them searchPost vao csdl Post
            crud_addpost._add_post(
                user, pw, url, db_name, searchPost, imagePath)

            # Tim kiem va tra ket qua
            findpost = FindPost()
            list_posts = findpost.get_all_post()
            print(searchPost)
            print(imagePath)
            print(list_posts)

            return render(request, 'find_lostdog/searchLostDog.html', {'searchPost': searchPost, 'listposts': list_posts, 'form': searchLostDogForm})

    else:
        searchLostDogForm = PostForm()
    return render(request, 'find_lostdog/searchLostDog.html', {'form': searchLostDogForm})
