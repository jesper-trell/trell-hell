import uuid

from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=160, blank=True)
    pub_date = models.DateTimeField('Date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    likes = models.ManyToManyField(User, through='Like', related_name='likes')

    def __str__(self):
        return self.title


class Like(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"'{self.user}' likes '{self.photo}'"
