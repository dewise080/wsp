from django.apps import AppConfig


class CustompageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custompage'

    def ready(self):
        from . import translation  # noqa
