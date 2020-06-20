import io
import os
import random
import datetime
import base64
import matplotlib.image as mpimg
import mysql.connector
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from mysql.connector import errorcode
from .forms import *
from django.http import HttpResponse
from .FP.main import FindPost
from PIL import Image
from pathlib import Path
from .forms import *
from .models import *
from .tool.findDogType import FindDogType
from .tool.CRUDdog import CRUD_Dog
from .FP.CRUDpost import CRUD_Post


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

# Change to your informations below


modelpath = r'/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/dog_classification_resnet.pth'
classnamepath = r'/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/class_names.pkl'
user = 'admin'
pw = 'mmx1437cbcd'
url = 'localhost'
db_name = 'muti_media_db'

# Search dog from tag and image


def getImageByName(dog_type):
    folder = "media/Images/"+dog_type
    images = []
    for i in range(6):
        img = random.choice(os.listdir(folder))
        img_url = "media/Images/"+dog_type+"/"+img
        images.append(img_url)
    # print(images)
    return images


def searchDog(request):
    list_dogtype = []
    list_dogimage = []
    if request.method == 'POST':
        dogForm = SearchDogForm(request.POST or None, request.FILES or None)
        if dogForm.is_valid():
            dogForm.save()

        # Khoi tao cac doi tuong control
        compare = FindDogType(modelpath, classnamepath, user, pw, url, db_name)
        crud_dog = CRUD_Dog(modelpath, classnamepath)
        crud_post = CRUD_Post()

        # Lay url anh
        Dogs = Image_db.objects.latest()

        if bool(Dogs.image) == True:
            dogPath = ("." + str(Dogs.image.url))
            path = Path(dogPath).resolve()
            # Chuyen anh sang dang binary
            image_bytes = crud_post.convertToBinaryData(path)
            image = Image.open(io.BytesIO(image_bytes))

            if bool(Dogs.tag) == False:
                results = compare._find_dog_type_from_img(image)
            else:
                results = compare.find_dog_type(image, str(Dogs.tag))
        elif bool(Dogs.tag) == True:
            results = compare._find_dog_type_from_tag(str(Dogs.tag))
            dogPath = None

        print(results)
        for result in results:
            dog = crud_dog._getDogByType(
                user, pw, url, db_name, result)  # Thong tin ket qua loai cho
            dogimage = getImageByName(result)  # Mang 2 hinh anh ket qua
            # list_dogtype += dog   # Dict cua cac loai cho tra ve
            ldog = list(dog[0])
            ldog[1] = ldog[1].split("-")[1]
            temp = {}
            temp["content"] = ldog
            temp["url"] = dogimage
            list_dogtype.append(temp)

        print(list_dogtype)
        print(dogPath)
        if(len(list_dogtype) > 0):
            first_dog = list_dogtype.pop(0)
            message = 'success'
        else:
            first_dog = None
            message = 'error'

        return render(request, 'find_lostdog/searchDog.html', {'listdogs': list_dogtype,
                                                               'first_dog': first_dog, 'img': dogPath, 'message': message, 'form': dogForm})
    else:
        dogForm = SearchDogForm()
        return render(request, 'find_lostdog/searchDog.html', {'form': dogForm})


# Add new post to find dog


def addPost(request):
    # submitbutton = request.POST.get("submit")
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
            addForm.save()

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
        return render(request, 'find_lostdog/post.html', {'image_url': imagePath, 'img': img_url, 'post': post, 'form': addForm})

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
    simage = []

    if request.method == 'POST':
        searchLostDogForm = SearchLostDogForm(request.POST, request.FILES)
        if searchLostDogForm.is_valid():
            searchLostDogForm.save()
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
        list_all = list_posts.values.tolist()
        # print(list_all)

        for i in range(0, len(list_all)):
            list_all[i][9] = base64.b64encode(list_all[i][9]).decode("utf-8")
            if i == 5:
                break

        # print(image)

        print(searchPost)
        print(imagePath)
        print(list_posts)

        return render(request, 'find_lostdog/searchLostDog.html', {'searchPost': searchPost, 'listposts': list_all, 'img': img_url, 'image': simage, 'form': searchLostDogForm})

    else:
        searchLostDogForm = PostForm()
        return render(request, 'find_lostdog/searchLostDog.html', {'form': searchLostDogForm})

def listPost(request):
    findpost = FindPost()
    list_posts = findpost.get_all_post()
    list_all = list_posts.values.tolist()
   
    for i in range(0, len(list_all)):
        list_all[i][9] = base64.b64encode(list_all[i][9]).decode("utf-8")
   
    return render(request, 'find_lostdog/post_list.html', {'listposts': list_all})