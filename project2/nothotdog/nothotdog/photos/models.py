import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_hashids import HashidsField


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=160,)
    description = models.CharField(max_length=160, blank=True)
    pub_date = models.DateTimeField('Date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    hashid = HashidsField(
                real_field_name="id",
                salt="salty jesper",
                min_length=10,
                editable=False,
            )

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)