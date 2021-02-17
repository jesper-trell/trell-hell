from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Like, Photo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'id',
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


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = [
            'user',
            'date',
        ]
