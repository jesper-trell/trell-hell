from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from nothotdog.photos.serializers import (LikeSerializer, PhotoSerializer,
                                          UserSerializer)
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from .models import Like, Photo


class TestView(TemplateView):
    template_name = 'frontend/test.html'


class LikesViewAPI(ListAPIView):
    def get_queryset(self):
        return Photo.objects.get(uu_id=self.kwargs['photo_uu_id'])

    def get(self, request, *args, **kwargs):
        photo = self.get_queryset()
        likes = Like.objects.filter(photo=photo)

        serializer = LikeSerializer(
            likes,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        photo = self.get_queryset()
        like = Like.objects.create(
            photo=photo,
            user=self.request.user,
            date=timezone.now()
        )
        like.save()

        return redirect('photos:photo', photo_uu_id=photo.uu_id)
        # return reverse(
        #     'photos:photo',
        #     kwargs={'photo_uu_id': photo.uu_id},
        # )

    # def post(self, request, *args, **kwargs):
    #     photo = Photo.objects.get(uu_id=self.kwargs['photo_uu_id'])
    #     like = Like.objects.create(photo=photo, user=self.request.user)
    #     like.save()


class UsersViewAPI(LoginRequiredMixin, ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PhotosViewAPI(LoginRequiredMixin, ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ConfigurablePaginationMixin:
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by') or self.paginate_by


class ExtraContext(object):
    extra_context = {'index_view': True}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class IndexView(ExtraContext, ConfigurablePaginationMixin, ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    queryset = model.objects.filter(flagged=False).order_by('-pub_date')
    paginate_by = 20


class ProfileView(
    ConfigurablePaginationMixin,
    LoginRequiredMixin,
    ListView
):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(
            flagged=False,
            user=self.request.user,
            ).order_by('-pub_date')


class PhotoView(TemplateView):
    template_name = 'photos/photo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = Photo.objects.get(uu_id=self.kwargs['photo_uu_id'])
        likes = Like.objects.filter(photo=photo)
        num_likes = len(likes)
        context['photo'] = photo
        context['num_likes'] = num_likes
        context['likes'] = likes
        return context


class EditView(LoginRequiredMixin, UpdateView):
    model = Photo
    template_name = 'photos/edit.html'
    fields = ['description']

    def get_success_url(self):
        return reverse(
            'photos:photo',
            kwargs={'photo_uu_id': self.kwargs['photo_uu_id']},
        )

    def get_object(self):
        return Photo.objects.get(uu_id=self.kwargs['photo_uu_id'])


class UploadView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'photos/upload.html'
    fields = [
        'image',
        'title',
        'description',
    ]

    def form_valid(self, form):
        self.photo = form.save(commit=False)
        self.photo.pub_date = timezone.now()
        self.photo.user = self.request.user

        return super(UploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'photos:photo',
            kwargs={'photo_uu_id': self.photo.uu_id},
        )

# def LikeView(request, photo_uu_id):
#     user = request.user
#     photo = Photo.objects.get(uu_id=photo_uu_id)
#     print(user)
#     print(photo)
#     from django.shortcuts import redirect
#     return redirect('photos:profile')
