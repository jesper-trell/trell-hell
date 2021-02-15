from django.http import HttpResponseRedirect
from django.urls import path, reverse

from . import views

app_name = 'photos'
urlpatterns = [
    path('', lambda r: HttpResponseRedirect(reverse('photos:index'))),
    path('photos', views.IndexView.as_view(), name='index'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('users_API', views.UsersViewAPI.as_view(), name='users_API'),
    path('photos_API', views.PhotosViewAPI.as_view(), name='photos_API'),
    path('test', views.TestView.as_view(), name='test'),
    path('<str:photo_uu_id>', views.PhotoView.as_view(), name='photo'),
    path('<str:photo_uu_id>/like', views.LikesViewAPI.as_view(), name='likes_API'),  # noqa
    path('<str:photo_uu_id>/edit', views.EditView.as_view(), name='edit'),
]
