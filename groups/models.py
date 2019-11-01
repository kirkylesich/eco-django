from django.db import models
from users.models import User
from pytils.translit import slugify


class Group(models.Model):
    image = models.ImageField(upload_to='groups_img', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    small_description = models.CharField(max_length=102, null=False, blank=False)
    description = models.TextField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="creater_group")
    members = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)

# Create your models here.
