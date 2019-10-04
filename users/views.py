from django.shortcuts import render
from django.shortcuts import redirect
from users.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.http import HttpResponse
import json
from django.http import JsonResponse


def show_forms_errors(request, form):
    for error in form.errors.as_data():
        messages.add_message(request, messages.ERROR, json.loads(form.errors.as_json())[error][0]['message'])


@login_required
def personaldata(request):
    user = request.user
    print(user.is_confirmed)
    form = PersonalData()
    return render(request, 'personalData.html', {'form': form, 'user': user})


@login_required
@require_POST
def personal_update(request):
    user = request.user
    form = PersonalData(request.POST, instance=user)
    if form.is_valid() and user.is_confirmed:
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Данные сохранены!')
    elif not user.is_confirmed:
        messages.add_message(request, messages.ERROR, 'Вам нужно подтвердить аккаунт чтобы изменять личные данные!')
    else:
        show_forms_errors(request, form)
    return render(request, 'personalData.html', {'form': form, 'user': user})

@require_POST
def change_password(request):
    user = request.user

    print(request.POST)
    return HttpResponse(request.POST)

