from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from nothotdog.photos.serializers import LikeSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Like, Photo
from .utilities import send_like_mail


class LikesViewAPI(ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(photo__uu_id=self.kwargs['uuid'])

    @action(detail=True, permission_classes=[IsAuthenticated])
    def post(self, request, *args, **kwargs):
        like = Like.objects.create(
            photo=Photo.objects.get(uu_id=self.kwargs['uuid']),
            user=self.request.user,
            date=now(),
        )
        send_like_mail(like)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        Like.objects.get(
            photo__uu_id=self.kwargs['uuid'],
            user=self.request.user,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfigurablePaginationMixin:
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', default=self.paginate_by)


class IndexView(ConfigurablePaginationMixin, ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', default='pub_date')
        return self.model.objects.annotate(
            num_likes=Count('likes')
        ).filter(
            flagged=False
        ).order_by('-' + order_by)


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
        order_by = self.request.GET.get('order_by', default='pub_date')
        return self.model.objects.annotate(
            num_likes=Count('likes')
        ).filter(
            flagged=False,
            user=self.request.user,
        ).order_by('-' + order_by)


class LikedView(
    ConfigurablePaginationMixin,
    LoginRequiredMixin,
    ListView
):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 30

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', default='pub_date')
        return self.model.objects.annotate(
            num_likes=Count('likes')
        ).filter(
            flagged=False,
            likes=self.request.user
        ).order_by('-' + order_by)


class PhotoView(DetailView):
    model = Photo
    template_name = 'photos/photo.html'
    slug_url_kwarg = 'uuid'
    slug_field = 'uu_id'


class EditView(LoginRequiredMixin, UpdateView):
    model = Photo
    template_name = 'photos/edit.html'
    fields = ['description']

    def get_success_url(self):
        return reverse(
            'photos:photo',
            kwargs={'uuid': self.kwargs['uuid']},
        )

    def get_object(self):
        return Photo.objects.get(uu_id=self.kwargs['uuid'])


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
        self.photo.pub_date = now()
        self.photo.user = self.request.user

        return super(UploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'photos:photo',
            kwargs={'uuid': self.photo.uu_id},
        )
