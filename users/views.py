from django.shortcuts import render
from users.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json


def show_forms_errors(request,form):
    for error in form.errors.as_data():
        messages.add_message(request, messages.ERROR, json.loads(form.errors.as_json())[error][0]['message'])

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
            show_forms_errors(request,form)
    return render(request,'personalData.html',{'form':form,'user':user})

def change_password(request):
    user = request.user