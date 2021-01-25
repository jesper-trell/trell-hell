from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UploadForm(forms.ModelForm): 
  
    class Meta: 
        model = Photo 
        fields = ['image',
                  'photo_title',
                  'photo_description',
                  ]


class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",) 
