from django.urls import path, include
from maineco.views import *
from users.views import *
app_name='maineco'

urlpatterns = [
    path('',main,name='index'),
    path('login/',loginuser,name='loginuser'),
    path('logout/',logout,name='logout'),
    path('signup/',signup,name='signup'),
    path('signup/verification/<hash_code>',validate_hash,name='hash_code'),
    path('joinevent/',join_event,name='join_event'),


    path('personal-data/',include('users.urls'))

    
]
