import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=160, blank=True)
    pub_date = models.DateTimeField('Date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # likes = models.ManyToManyField(User, through='Like')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Like(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"'{self.user}' likes '{self.photo}'"


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
#     date = models.DateTimeField()
