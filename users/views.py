from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.shortcuts import redirect
from users.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.http import HttpResponse
import json
from groups.models import Group
from django.http import JsonResponse


def show_forms_errors(request, form):
    for error in form.errors.as_data():
        messages.add_message(request, messages.ERROR, json.loads(form.errors.as_json())[error][0]['message'])


@login_required
def personaldata(request):
    user = request.user
    form = PersonalData()
    form_pass = PasswordChangeForm(user)
    groups = Group.objects.filter(creater=user)
    return render(request, 'lk.html', {'form_pass': form_pass, 'form': form, 'user': user, 'groups': groups})


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
    form = PersonalData(instance=user)
    form_pass = PasswordChangeForm(user, request.POST)
    if form_pass.is_valid():
        user = form_pass.save()
        update_session_auth_hash(request, user)
        messages.add_message(request, messages.SUCCESS, 'Пароль изменён!')
    else:
        show_forms_errors(request, form_pass)
    return render(request, 'personalData.html', {'form_pass': form_pass, 'form': form, 'user': user})
