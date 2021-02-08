from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Photo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = [
            'image',
            'title',
            'description',
            'flagged',
            'uu_id',
        ]
