import pika
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import generic

from .forms import *
from .models import Photo


class IndexView(generic.ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get(self, request):
        paginate_by = request.GET.get('paginate_by') or self.paginate_by
        data = self.model.objects.filter(flagged=False)

        paginator = Paginator(data, paginate_by)
        page = request.GET.get('page')
        paginated = paginator.get_page(page)

        return render(request, 'photos/index.html', {'photos_list': paginated})


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = Photo
    template_name = 'photos/index.html'
    context_object_name = 'photos_list'
    paginate_by = 20

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user, flagged=False)

    def get(self, request):
        paginate_by = request.GET.get('paginate_by') or self.paginate_by
        data = self.model.objects.filter(user=self.request.user, flagged=False)

        paginator = Paginator(data, paginate_by)
        page = request.GET.get('page')
        paginated = paginator.get_page(page)

        return render(request, 'photos/index.html', {'photos_list': paginated})


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
            form = form.save(commit=False)
            form.pub_date = timezone.now()
            form.user = request.user
            form.save()

            photo = Photo.objects.get(hashid=form.hashid)

            is_hotdog = 'hotdog' in photo.title.lower()
            if not is_hotdog:
                send_alert_message(photo.title)

            context = {
                'photo': photo,
            }

            return render(request, 'photos/photo.html', context)
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form' : form})


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
    channel.basic_publish(exchange='', routing_key='hotdog_alert', body=message)
    print(" [x] Image not depicting hot dog has been spotted!'")
    connection.close()
