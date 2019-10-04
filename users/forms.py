from django.forms import ModelForm
from users.models import User


class PersonalData(ModelForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email']
        error_messages = {
            'phone': {
                'unique': "Пользователь с таким номером телефона уже существует!",
            },
        }
