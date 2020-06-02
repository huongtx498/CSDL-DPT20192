from django.urls import path
from django.urls import path, include
from .views import *
from find_lostdog.views import *

urlpatterns = [

]

urlpatterns = [
    path('findDog', find_doginfo, name='findPOSTpage'),
    path('post', index, name='postLostDog'),
    path('searchLostDog', searchLostDog, name='searchLostDog'),
    path('', searchDog, name='searchDog'),
]
