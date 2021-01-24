from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Photo
from .forms import *


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

def upload(request): 
    if request.method == 'POST': 
        form = UploadForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form = form.save(commit=False)
            form.pub_date = timezone.now()
            form.save() 
            return redirect('success') 
    else: 
        form = UploadForm() 
    return render(request, 'photos/upload.html', {'form' : form}) 
  
  
def success(request): 
    return HttpResponse('Successfully uploaded')
