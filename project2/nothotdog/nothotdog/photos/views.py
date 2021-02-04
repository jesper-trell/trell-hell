import pika
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from .forms import PhotoEditForm, PhotoUploadForm
from .models import Photo


class ConfigurablePaginationMixin:
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by') or self.paginate_by


class ExtraContext(object):
    extra_context = {'index_view': True}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class IndexView(ExtraContext, ConfigurablePaginationMixin, generic.ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    queryset = model.objects.filter(flagged=False).order_by('-pub_date')
    paginate_by = 20


class ProfileView(
    ConfigurablePaginationMixin,
    LoginRequiredMixin,
    generic.ListView
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


def photo(request, photo_uu_id):
    photo = Photo.objects.get(uu_id=photo_uu_id)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required
def upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.pub_date = timezone.now()
            photo.user = request.user
            photo.save()

            return render(request, 'photos/photo.html', {'photo': photo})
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})


@login_required
def edit(request, photo_uu_id):
    photo = Photo.objects.get(uu_id=photo_uu_id)

    if request.user != photo.user:
        return redirect('photos:photo', photo_uu_id=photo_uu_id)

    if request.method == 'POST':
        form = PhotoEditForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photos:photo', photo_uu_id=photo_uu_id)
    else:
        form = PhotoEditForm(instance=photo)

    context = {
        'photo': photo,
        'form': form,
    }

    return render(request, 'photos/edit.html', context)


def send_photo_alert(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue='hotdog_alert')
    channel.basic_publish(
        exchange='',
        routing_key='hotdog_alert',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent.
        )
    )
    connection.close()


@receiver(post_save, sender=Photo)
def callback(sender, instance, created, **kwargs):
    # Do nothing if there was no new upload.
    if created:
        bytes_data = (instance.id).to_bytes(2, byteorder='big')
        send_photo_alert(bytes_data)
