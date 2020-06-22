from django.urls import path
from django.urls import path, include
from .views import *
from find_lostdog.views import *

urlpatterns = [

]

urlpatterns = [
    path('post', addPost, name='postLostDog'),
    path('listPost' ,listPost, name='listPost'),
    path('searchLostDog', searchLostDog, name='searchLostDog'),
    path('', searchDog, name='searchDog'),
]
