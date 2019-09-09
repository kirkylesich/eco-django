from django.shortcuts import render,redirect
from maineco.models import Event
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth

def main(request):
    print(request.user)
    events = Event.objects.all()
    return render(request,'index.html',{'events':events,'user':request.user})

def loginuser(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)    
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            errors='Неправильно введены данные'
            return render(request,'login.html',{'error':errors})
    return render(request,'login.html')


def signup(request):
    print(request.POST)
    return render(request,'registration.html')

def logout(request):
    auth.logout(request)
    return redirect('/')