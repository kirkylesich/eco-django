from django.urls import path, include
from maineco.views import *

app_name='maineco'

urlpatterns = [
    path('',main,name='index'),
    path('login/',loginuser,name='loginuser'),
    path('logout/',logout,name='logout'),
    path('signup/',signup,name='signup'),
    
]
