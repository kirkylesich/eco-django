from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

