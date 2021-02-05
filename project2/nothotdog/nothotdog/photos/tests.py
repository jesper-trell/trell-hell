from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Photo


class PhotoTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'test_user',
            'test_user@test.com',
            'pass'
        )

    def test_photo_no_description(self):
        photo = Photo.objects.create(
            title='title',
            pub_date=timezone.now(),
            user=self.test_user,
        )
        self.assertEqual(photo.description, '')
