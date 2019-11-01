from django.urls import path, include
from maineco.views import *
from users.views import *

app_name = 'maineco'

urlpatterns = [
    path('', personaldata, name="personal_data"),
    path('update/',personal_update,name="personal_update"),
    path('change_password/',change_password,name='change_password')
]
