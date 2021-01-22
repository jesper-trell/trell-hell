from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:photo_hashid>', views.photo, name='photo'),
]