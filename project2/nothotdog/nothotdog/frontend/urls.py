from django.urls import path
from . import views


app_name = 'frontend'
urlpatterns = [
    path('test', views.index, name='index'),
]
