from django.http import HttpResponseRedirect
from django.urls import path, reverse

from . import views

app_name = 'photos'
urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse('photos:index'))),
    path('photos', views.IndexView.as_view(), name='index'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('<str:photo_uu_id>', views.PhotoView.as_view(), name='photo'),
    path('<str:photo_uu_id>/edit', views.EditView.as_view(), name='edit'),
]
