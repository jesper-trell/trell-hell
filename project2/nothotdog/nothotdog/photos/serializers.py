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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            'image',
            'title',
            'description',
            'pub_date',
            # 'user',
            'flagged',
            'uu_id',
        ]

    def get_image_url(self, obj):
        return obj.image.url
