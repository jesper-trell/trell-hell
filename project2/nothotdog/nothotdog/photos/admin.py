from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_title', 'pub_date', 'user')


admin.site.register(Photo, PhotoAdmin)