# Generated by Django 2.2 on 2019-09-23 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190907_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hash_code',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
