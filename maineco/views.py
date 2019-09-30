from django.shortcuts import render, redirect
from maineco.models import Event
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from users.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse


def gen_hash():
    hash_user = str(uuid.uuid4())
    return hash_user.replace("-", "")


def main(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events, 'user': request.user})


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
            errors = 'Неправильно введены данные'
            return render(request, 'login.html', {'error': errors})
    return render(request, 'login.html')


def sendemail(email, hash_code, request):
    baseurl = request.scheme + ':' + request.META['HTTP_HOST']
    message = render_to_string('mail/message.html', {'hash': hash_code, "baseurl": baseurl})
    send_mail(subject='Добро пожаловать !', message=" ",
              from_email=settings.EMAIL_HOST_USER, recipient_list=[email, ], fail_silently=False, html_message=message)


def validate_hash(request, hash_code):
    user = get_object_or_404(User, hash_code=hash_code)
    user.is_confirmed = True
    user.hash_code = 0
    user.save()
    return redirect('/')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password_new = request.POST['password_new']
        password_confirmed = request.POST['password_confirmed']
        if password_new == password_confirmed:
            try:
                User.objects.get(email=username)
                return render(request, 'registration.html', {"error": "Аккаунт с таким адресом уже существует"})
            except:
                user = User(email=username)
                user.hash_code = gen_hash()
                user.save()
                user.set_password(password_new)
                user.save()
                sendemail(user.email, user.hash_code, request)
                user = authenticate(request, username=username, password=password_new)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            return render(request, 'registration.html', {"error": "Пароли не совпадают"})
    return render(request, 'registration.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def join_event(request):
    if request.is_ajax():
        event = Event.objects.get(id=request.POST['id_event'])
        try:
            if request.user.is_invited(event):
                message = "Вы уже записаны!"
                tag = 'error'
            else:
                message = "Вы успешно записались!"
                tag = 'success'
                event = Event.objects.get(id=request.POST['id_event'])
                event.members.add(request.user)
        except:
            message = "Что то пошло не так"
            tag = "error"
    return JsonResponse({'message': message, "tag": tag, "member_count": event.get_count_members(),"id_event":event.id}, safe=False)
