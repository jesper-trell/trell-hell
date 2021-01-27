from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upload', views.upload, name='upload'),
    path('<str:photo_hashid>', views.photo, name='photo'),
    path('<str:photo_hashid>/edit', views.edit, name='edit'),
]