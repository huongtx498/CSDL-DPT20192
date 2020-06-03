import io
import os
import mysql.connector
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from mysql.connector import errorcode
from .forms import *
from django.http import HttpResponse
from find_lostdog.FP.main import FindPost
from PIL import Image
from pathlib import Path
from .forms import *
from .models import *
from find_lostdog.tool.findDogType import FindDogType
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


def searchDog(request):
    list_dogtype = []

    if request.method == 'POST':
        dogForm = SearchDogForm(request.POST or None, request.FILES or None)
        if dogForm.is_valid():
            dogForm.save()
    else:
        dogForm = SearchDogForm()
    Dogs = Image_db.objects.latest()
    # dogPath = os.path.join("", str(Dogs.image.url))
    # path = Path(dogPath).resolve()
    x = "media/images/n02085620_242.jpg"
    path = Path(x).resolve()
    compare = FindDogType(modelpath, classnamepath, user, pw, url, db_name)
    crud_dog = CRUD_Dog(modelpath, classnamepath)
    crud_post = CRUD_Post()

    image_bytes = crud_post.convertToBinaryData(path)
    image = Image.open(io.BytesIO(image_bytes))
    results = compare._find_dog_type_from_tag(Dogs.tag)
    # results = compare._find_dog_type_from_img(image)
    # results = compare.find_dog_type(image, str(Dogs.tag))
    for result in results:
        list_dogtype.append(crud_dog._getDogByType(user, pw,
                                                   url, db_name, result))
    print(results)
#  'image': Dogs
    return render(request, 'find_lostdog/searchDog.html', {'context': list_dogtype, 'path': path, 'form': dogForm})


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
            image0 = request.FILES['dogImage']
            fs = FileSystemStorage()
            filename = fs.save(image0.name, image0)
            image_url = fs.url(filename)
            # image_url = addForm.cleaned_data['dogImage']
            spiece = addForm.cleaned_data.get('species')
            weights = addForm.cleaned_data.get('weight')
            heights = addForm.cleaned_data.get('height')
            colors = addForm.cleaned_data.get('color')
            access = addForm.cleaned_data.get('accessory')
            area = addForm.cleaned_data.get('location')
            time = addForm.cleaned_data.get('time')
            status = addForm.cleaned_data.get('status')

            x = "media/images/n02085620_242.jpg"
            path = Path(x).resolve()
            post = Post(spiece, weights, heights, colors,
                        access, area, time, status, type)
            crud_addpost = CRUD_Post()
            # crud_addpost._add_post(user, pw, url, db_name, post, image_url)
            print(post)
            print(image_url)

    else:
        addForm = PostForm()

    return render(request, 'find_lostdog/post.html', {'image': image_url, 'post': post, 'form': addForm})


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
            image0 = request.FILES['dogImage']
            fs = FileSystemStorage()
            filename = fs.save(image0.name, image0)
            image_url = fs.url(filename)
            # image_url = searchLostDogForm.cleaned_data['dogImage']
            spiece = searchLostDogForm.cleaned_data.get('species')
            weights = searchLostDogForm.cleaned_data.get('weight')
            heights = searchLostDogForm.cleaned_data.get('height')
            colors = searchLostDogForm.cleaned_data.get('color')
            access = searchLostDogForm.cleaned_data.get('accessory')
            area = searchLostDogForm.cleaned_data.get('location')
            time = searchLostDogForm.cleaned_data.get('time')
            status = searchLostDogForm.cleaned_data.get('status')

        x = "media/images/n02085620_242.jpg"
        path = Path(x).resolve()
        post = Post(spiece, weights, heights, colors,
                    access, area, time, status, type)
        crud_addpost = CRUD_Post()
        # crud_addpost._add_post(user, pw, url, db_name, post, image_url)
        findpost = FindPost()
        list_posts = findpost.get_all_post()
        print(post)
        print(image_url)

    else:
        searchLostDogForm = PostForm()
    return render(request, 'find_lostdog/searchLostDog.html', {'post': post, 'list_posts': list_posts, 'form': searchLostDogForm})
