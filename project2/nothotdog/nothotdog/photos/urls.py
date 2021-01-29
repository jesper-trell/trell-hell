from django.http import HttpResponseRedirect
from django.urls import path, reverse

from . import views

app_name = 'photos'
urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse('photos:index'))),
    path('photos', views.IndexView.as_view(), name='index'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upload', views.upload, name='upload'),
    path('<str:photo_uu_id>', views.photo, name='photo'),
    path('<str:photo_uu_id>/edit', views.edit, name='edit'),
]
