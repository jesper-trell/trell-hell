from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Photo


class PhotoTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            'test_user',
            'test_user@test.com',
            'pass'
        )
        Photo.objects.create(
            # image=,
            title="title",
            description="description",
            pub_date=timezone.now(),
            user=test_user,
            flagged=False,
        )

    # Printing a Photo displays the title.
    def test_photo_prints_title(self):
        photo = Photo.objects.get(title="title")
        self.assertEqual(str(photo), 'title')


class PaginatorTestCase(TestCase):
    def setUp(self):
        pass

    def test_(self):
        pass
