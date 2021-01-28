import pika
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from .forms import PhotoEditForm, PhotoUploadForm
from .models import Photo


class ConfigurablePaginationMixin:
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by') or self.paginate_by


class IndexView(generic.ListView, ConfigurablePaginationMixin):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    queryset = model.objects.filter(flagged=False)
    paginate_by = 20


class ProfileView(LoginRequiredMixin, generic.ListView, ConfigurablePaginationMixin):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(flagged=False, user=self.request.user)


def photo(request, photo_hashid):
    photo = Photo.objects.get(hashid=photo_hashid)

    context = {
        'photo': photo,
    }

    return render(request, 'photos/photo.html', context)


@login_required
def upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            photo = form.save(commit=False)
            photo.pub_date = timezone.now()
            photo.user = request.user
            photo.save()

            # photo = Photo.objects.get(hashid=form.hashid)

            is_hotdog = 'hotdog' in photo.title.lower()
            if not is_hotdog:
                send_alert_message(photo.hashid)

            context = {
                'photo': photo,
            }

            return render(request, 'photos/photo.html', context)
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})


@login_required
def edit(request, photo_hashid):
    photo = Photo.objects.get(hashid=photo_hashid)

    if request.user != photo.user:
        return redirect('/photos/' + photo_hashid)

    if request.method == 'POST':
        form = PhotoEditForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('/photos/' + photo_hashid)
    else:
        form = PhotoEditForm(instance=photo)

    context = {
        'photo': photo,
        'form': form,
    }

    return render(request, 'photos/edit.html', context)


def send_alert_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
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
    print(" [x] Image not depicting hot dog has been spotted!'")
    connection.close()
