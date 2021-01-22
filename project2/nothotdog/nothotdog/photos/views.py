from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from .models import Photo


def index(request):
    photos_list = Photo.objects.order_by('-pub_date')[:]
    context = {
        'photos_list': photos_list,
        }
    return render(request, 'photos/index.html', context)


def photo(request, photo_hashid):
    photo = Photo.objects.get(hashid=photo_hashid)

    context = {
        'photo': photo,
        }
    
    return render(request, 'photos/photo.html', context)
