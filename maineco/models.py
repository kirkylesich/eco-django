from django.db import models
from users.models import User
# Create your models here.


class Event(models.Model):
    image = models.ImageField(upload_to='events_img', height_field=None, width_field=None, max_length=None,null=True,blank=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    date_create = models.DateTimeField(auto_now_add=True,)
    date_start = models.DateTimeField(auto_now=False,null=True,blank=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE,null=False,blank=False,related_name="creater")
    members = models.ManyToManyField(User)

    def get_count_members(self):
        count = self.members.all().count()
        return count




