from django.apps import AppConfig


class PhotosConfig(AppConfig):
    name = 'nothotdog.photos'

    def ready(self):
        import nothotdog.photos.signals.upload_handler  # noqa