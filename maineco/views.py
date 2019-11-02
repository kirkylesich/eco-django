from django.shortcuts import render, redirect
from django.urls import reverse

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
from groups.models import Group
from django.contrib.auth.forms import UserCreationForm
from maineco.forms import SignUpForm
from users.views import show_forms_errors
from django.views.decorators.http import require_POST, require_GET
from django.contrib.sites.shortcuts import get_current_site


def gen_hash():
    hash_user = str(uuid.uuid4())
    return hash_user.replace("-", "")


def main(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('about/')


def about(request):
    print(request.get_host())
    print(request.scheme)
    groups = Group.objects.all()
    return render(request, 'about.html', {'groups': groups, 'user': request.user})


def loginuser(request):
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/personal-data/')
        else:
            errors = 'Неправильно введены данные'
            return render(request, 'login.html', {'error': errors})
    return render(request, 'login.html')


def sendemail(email, hash_code, request):
    baseurl = request.scheme + '://' + request.get_host()
    message = render_to_string('mail/message.html', {'hash': hash_code, "baseurl": baseurl})
    send_mail(subject='Добро пожаловать !', message=" ",
              from_email='clear-ufa@info.ru', recipient_list=[email, ], fail_silently=False, html_message=message)


def validate_hash(request, hash_code):
    if hash_code != "0":
        user = get_object_or_404(User, hash_code=hash_code)
        user.is_confirmed = True
        user.hash_code = 0
        user.save()
    else:
        return redirect('/')
    return redirect('/personal-data/')


def signup(request):
    form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


@require_POST
def signup_user(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        user.hash_code = gen_hash()
        user.save()
        sendemail(user.email, user.hash_code, request)
        login(request, user)
        return redirect('/personal-data/')
    else:
        show_forms_errors(request, form)
        return render(request, 'registration.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


def join_event(request):
    status = 202
    user = request.user
    if request.is_ajax():
        event = Event.objects.get(id=request.POST['id_event'])
        if user.is_authenticated:
            if user.is_invited(event):
                message = "Вы уже записаны!"
                tag = 'error'
            elif not user.is_confirmed:
                message = "Вы должны подтвердить свой аккаунт для того чтобы учавстовать в мероприятии"
                tag = 'error'
                status = 424
            else:
                message = "Вы успешно записались!"
                tag = 'success'
                event = Event.objects.get(id=request.POST['id_event'])
                event.members.add(user)
        else:
            message = 'Авторизуйтесь или зарегистрируйтесь для того чтобы учавстовать в мероприятиях!'
            tag = 'error'
            status = 401
    return JsonResponse(
        {'message': message, "tag": tag, "member_count": event.get_count_members(), "id_event": event.id}, safe=False,
        status=status)
