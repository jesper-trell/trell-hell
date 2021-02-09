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
    image = serializers.SerializerMethodField(read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    def get_image(self, obj):
        # obj is model instance
        return obj.image.url

    # def get_username(self, obj):
    #     # obj is model instance
    #     return obj.username.username

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
