from django.apps import AppConfig


class SampleconversationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sampleconversations'

    def ready(self):
        # Ensure components are registered on startup.
        from . import components  # noqa: F401
        from . import signals  # noqa: F401
