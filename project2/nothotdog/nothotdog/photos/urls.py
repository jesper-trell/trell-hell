from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('image_upload', views.upload, name = 'image_upload'),
    path('success', views.success, name = 'success'),
    path('<str:photo_hashid>', views.photo, name='photo'),
]