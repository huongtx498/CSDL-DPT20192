import io
import os
import mysql.connector
from django.shortcuts import render, redirect
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

# Create your views here.


def index(request):
    if request.method == 'POST':
        response = HttpResponse()

        return response

    postForm = PostForm()
    return render(request, 'find_lostdog/post.html', {'form': postForm})


def searchLostDog(request):
    if request.method == 'POST':
        response = HttpResponse()

        return response

    searchLostDogForm = SearchLostDogForm()
    return render(request, 'find_lostdog/searchLostDog.html', {'form': searchLostDogForm})


def searchDog(request):
    if request.method == 'POST':
        response = HttpResponse()

        return response

    searchDogForm = SearchDogForm()
    return render(request, 'find_lostdog/searchDog.html', {'form': searchDogForm})

# Find post


def find_doginfo(request):
    findpost = FindPost()
    listpost = findpost.get_all_post()
    if request.method == 'POST':
        post_data = request.POST.dict()

    return render(request, 'find_lostdog/searchLostDog.html')

# Find dog by iddog_type


def find_doginfo(request):
    tag = None
    img = None
    post = None
    postForm = Post()
    if request.method == 'POST':
        postForm = Post(request.POST or None)
        post = dict(tag=(request.POST['spiece']))
    context = {
        'post': post,
    }

    return render(request, 'find_lostdog/posthome.html', {'context': context, 'form': postForm})


modelpath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL_DPT/CSDL-DPT/DPT/find_lostdog/tool/dog_classification_resnet.pth'
classnamepath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL_DPT/CSDL-DPT/DPT/find_lostdog/tool/class_names.pkl'
user = 'admin'
pw = 'mmx1437cbcd'
url = 'localhost'
db_name = 'muti_media_db'

# Find dog by iddog_type


def search_doginfo(request):
    list_dogtype = []
    dogForm = DogInfo()
    if request.method == 'POST':
        dogForm = DogInfo(request.POST or None, request.FILES or None)
        if dogForm.is_valid():
            dogForm.save()
        else:
            dogForm = DogInfo()
    Dogs = Image_db.objects.latest()
    dogPath = os.path.join("", str(Dogs.image.url))
    # path = Path(dogPath).resolve()
    print(Dogs)
    path = Path("media/images/n02085620_242.jpg").resolve()
    compare = FindDogType(modelpath, classnamepath)
    crud_dog = CRUD_Dog(modelpath, classnamepath)
    with open(path, 'rb') as f:
        image_bytes = f.read()
        image = Image.open(io.BytesIO(image_bytes))
        # result = compare.find_dog_type(image, str(Dogs.tag))
        results = compare._find_dog_type_from_tag(Dogs.tag)
        for result in results:
            list_dogtype.append(crud_dog._getDogByType(user, pw,
                                                       url, db_name, result))
    print(results)

    return render(request, 'find_lostdog/searchDog', {'image': Dogs, 'context': list_dogtype, 'path': path, 'image_': Dogs.image.url, 'form': dogForm})
