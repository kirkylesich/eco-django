from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    username=None
    phone = models.CharField(unique=True, max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    date_birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=False, blank=False,unique=True)
    hash_code = models.CharField(unique=True, max_length=200, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_invited(self,event):
        if self in event.members.all():
            return True
        else:
            return False