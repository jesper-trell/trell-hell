from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
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
        return Like.objects.filter(photo__uu_id=self.kwargs['photo_uu_id'])

    @action(detail=True, permission_classes=[IsAuthenticated])
    def post(self, request, *args, **kwargs):
        like = Like.objects.create(
            photo=Photo.objects.get(uu_id=self.kwargs['photo_uu_id']),
            user=self.request.user,
            date=timezone.now(),
        )
        send_like_mail(like)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        Like.objects.get(
            photo__uu_id=self.kwargs['photo_uu_id'],
            user=self.request.user,
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConfigurablePaginationMixin:
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by') or self.paginate_by


class ExtraContext(object):
    def get_context_data(self, **kwargs):
        self.extra_context = {
            'view': self.request.resolver_match.func.__name__
        }
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class IndexView(ExtraContext, ConfigurablePaginationMixin, ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        order_by = self.request.GET.get('order_by') or 'pub_date'
        return self.model.objects.annotate(
            num_likes=models.Count('likes')
        ).filter(
            flagged=False
        ).order_by('-' + order_by)


class ProfileView(
    ExtraContext,
    ConfigurablePaginationMixin,
    LoginRequiredMixin,
    ListView
):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        order_by = self.request.GET.get('order_by') or 'pub_date'
        return self.model.objects.annotate(
            num_likes=models.Count('likes')
        ).filter(
            flagged=False,
            user=self.request.user,
        ).order_by('-' + order_by)


class LikedView(
    ExtraContext,
    ConfigurablePaginationMixin,
    LoginRequiredMixin,
    ListView
):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 30

    def get_queryset(self):
        order_by = self.request.GET.get('order_by') or 'pub_date'
        return self.model.objects.annotate(
            num_likes=models.Count('likes')
        ).filter(
            flagged=False,
            likes=self.request.user
        ).order_by('-' + order_by)


class PhotoView(TemplateView):
    template_name = 'photos/photo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = Photo.objects.prefetch_related('likes').annotate(
            num_likes=models.Count('likes'),
            username=models.F('user__username')
        ).get(uu_id=self.kwargs['photo_uu_id'])

        context['photo'] = photo
        context['num_likes'] = photo.num_likes
        context['likes'] = photo.likes
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
