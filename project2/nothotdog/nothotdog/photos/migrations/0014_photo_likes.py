# Generated by Django 3.1.5 on 2021-02-26 12:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0013_auto_20210223_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='likes',
            field=models.ManyToManyField(related_name='photos', through='photos.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
