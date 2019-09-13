from django.shortcuts import render,redirect
from maineco.models import Event
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from users.models import User

def main(request):
    print(request.user)
    events = Event.objects.all()
    return render(request,'index.html',{'events':events,'user':request.user})

def loginuser(request):
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)    
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            errors='Неправильно введены данные'
            return render(request,'login.html',{'error':errors})
    return render(request,'login.html')


def signup(request):
    print(request.POST)
    if request.method == "POST":
        username = request.POST['username']
        password_new = request.POST['password_new']
        password_confirmed = request.POST['password_confirmed']
        if password_new == password_confirmed:
            try:
                User.objects.get(email=username)
                return render(request,'registration.html',{"error":"Аккаунт с таким адресом уже существует"})
            except:
                user=User(email=username)
                user.save()
                user.set_password(password_new)
                user.save()
                user = authenticate(request, username=username, password=password_new)  
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            return render(request,'registration.html',{"error":"Пароли не совпадают"})
    return render(request,'registration.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def personaldata(request):
    return render(request,'personalData.html')