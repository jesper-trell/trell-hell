from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'user',
        'flagged',
    )


admin.site.register(Photo, PhotoAdmin)
