from django.shortcuts import render
from users.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def personaldata(request):
    user = request.user
    form = PersonalData()
    if request.method == "POST":
        form = PersonalData(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Данные сохранены!')
        else:
            for error in form.errors:
                if error == "email":
                    messages.add_message(request, messages.ERROR, 'Введите правильный адрес электронной почты!')
                if error == "phone":
                    messages.add_message(request, messages.ERROR, 'Пользователь с таким телефоном уже существует!')

    return render(request,'personalData.html',{'form':form,'user':user})

def change_password(request):
    user = request.user