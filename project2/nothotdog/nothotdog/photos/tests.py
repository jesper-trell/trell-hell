from unittest.mock import patch

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


@patch('nothotdog.photos.signals.upload_handler.send_photo_alert')
class PhotoCreationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'

    def test_photo_no_description(self, mocked_alert):
        photo = create_photo(title=self.title1, user=self.user, flagged=False)
        self.assertEqual(mocked_alert.call_count, 1)
        self.assertEqual(photo.description, '')


@patch('nothotdog.photos.signals.upload_handler.send_photo_alert')
class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'
        cls.title2 = 'title2'

    def test_no_photos(self, mocked_alert):
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(mocked_alert.call_count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No photos are available.')
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [],
        )

    def test_unflagged_photo(self, mocked_alert):
        create_photo(title=self.title1, user=self.user, flagged=False)
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(mocked_alert.call_count, 1)
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title1}>'],
        )

    def test_flagged_photo(self, mocked_alert):
        create_photo(title=self.title1, user=self.user, flagged=True)
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(mocked_alert.call_count, 1)
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [],
        )

    def test_unflagged_and_flagged_photo(self, mocked_alert):
        create_photo(title=self.title1, user=self.user, flagged=False)
        create_photo(title=self.title2, user=self.user, flagged=True)
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(mocked_alert.call_count, 2)
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title1}>']
        )

    def test_two_unflagged_photos(self, mocked_alert):
        create_photo(title=self.title1, user=self.user, flagged=False)
        create_photo(title=self.title2, user=self.user, flagged=False)
        response = self.client.get(reverse('photos:index'))
        self.assertEqual(mocked_alert.call_count, 2)
        self.assertQuerysetEqual(
            response.context['photos_list'],
            [f'<Photo: {self.title2}>', f'<Photo: {self.title1}>']
        )


@patch('nothotdog.photos.signals.upload_handler.send_photo_alert')
class PhotoViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('test_user')
        cls.title1 = 'title1'
        cls.title2 = 'title2'

    def test_unflagged_photo(self, mocked_alert):
        unflagged_photo = create_photo(
            title=self.title1,
            user=self.user,
            flagged=False,
        )
        response = self.client.get(
            reverse('photos:photo', args=(unflagged_photo.uu_id,))
        )
        self.assertEqual(mocked_alert.call_count, 1)
        self.assertContains(response, unflagged_photo.title)

    def test_flagged_photo(self, mocked_alert):
        flagged_photo = create_photo(
            title=self.title1,
            user=self.user,
            flagged=True,
        )
        response = self.client.get(
            reverse('photos:photo', args=(flagged_photo.uu_id,))
        )
        self.assertEqual(mocked_alert.call_count, 1)
        self.assertEqual(response.status_code, 404)
