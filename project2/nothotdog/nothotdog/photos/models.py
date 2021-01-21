import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

class Photo(models.Model):
    photo_title = models.CharField(max_length=160)
    photo_description = models.CharField(max_length=160)
    pub_date = models.DateTimeField('Date published')
    photo = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.photo_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
