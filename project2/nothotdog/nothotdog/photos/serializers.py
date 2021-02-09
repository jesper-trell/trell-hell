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
    # user_name = serializers.RelatedField(source='user', read_only=True)

    def get_image(self, obj):
        # obj is model instance
        return obj.image.url

    # def get_user_name(self, obj):
    #     # obj is model instance
    #     return obj.user.username

    class Meta:
        model = Photo
        fields = [
            'image',
            'title',
            'description',
            'pub_date',
            # 'user_name',
            'flagged',
            'uu_id',
        ]
