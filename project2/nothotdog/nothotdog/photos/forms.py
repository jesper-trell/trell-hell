from django import forms 
from .models import *
  
class UploadForm(forms.ModelForm): 
  
    class Meta: 
        model = Photo 
        fields = ['image',
                  'photo_title',
                  'photo_description',
                  'user',
                  ]