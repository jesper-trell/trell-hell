from django.contrib import admin

from .models import Like, Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'uu_id',
        'pub_date',
        'user',
        'flagged',
    )


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'user',
        'photo',
    )


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Like, LikeAdmin)
