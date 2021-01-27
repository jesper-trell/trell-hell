from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = [
            'image',
            'title',
            'description',
        ]


class PhotoEditForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = [
            'description',
        ]


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)