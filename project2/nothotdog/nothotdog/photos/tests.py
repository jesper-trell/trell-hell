from unittest.mock import Mock, PropertyMock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Photo


def create_photo(title, user, flagged):
    return Photo.objects.create(
        image='/media/images/photo2.png',
        title=title,
        user=user,
        flagged=flagged,
        pub_date=timezone.now(),
    )


def create_user(username):
    return User.objects.create_user(
            username=username,
            email=f'{username}@email.com',
        )


class PhotoCreationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'

    def test_photo_no_description(self):
        photo = create_photo(title=self.title1, user=self.user, flagged=False)
        self.assertEqual(photo.description, '')


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'
        cls.title2 = 'title2'

    def test_no_photos(self):
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No photos are available.')
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [],
        )

    def test_unflagged_photo(self):
        create_photo(title=self.title1, user=self.user, flagged=False)
        response = self.client.get(reverse('photos:index'))
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title1}>'],
        )

    def test_flagged_photo(self):
        create_photo(title=self.title1, user=self.user, flagged=True)
        response = self.client.get(reverse('photos:index'))
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [],
        )

    def test_unflagged_and_flagged_photo(self):
        create_photo(title=self.title1, user=self.user, flagged=False)
        create_photo(title=self.title2, user=self.user, flagged=True)
        response = self.client.get(reverse('photos:index'))
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title1}>']
        )

    def test_two_unflagged_photos(self):
        create_photo(title=self.title1, user=self.user, flagged=False)
        create_photo(title=self.title2, user=self.user, flagged=False)
        response = self.client.get(reverse('photos:index'))
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title2}>', f'<Photo: {self.title1}>']
        )


class PhotoViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'
        cls.title2 = 'title2'

    def test_unflagged_photo(self):
        unflagged_photo = create_photo(
            title=self.title1,
            user=self.user,
            flagged=False,
        )
        response = self.client.get(
            reverse('photos:photo', args=(unflagged_photo.uu_id,))
        )
        self.assertContains(response, unflagged_photo.title)

    def test_flagged_photo(self):
        flagged_photo = create_photo(
            title=self.title1,
            user=self.user,
            flagged=True,
        )
        response = self.client.get(
            reverse('photos:photo', args=(flagged_photo.uu_id,))
        )
        self.assertEqual(response.status_code, 404)
