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
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Photo
        fields = [
            'image',
            'title',
            'description',
            'pub_date',
            'username',
            'flagged',
            'uu_id',
        ]
