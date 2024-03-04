from django.apps import AppConfig


class BuslinesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BusLinesApp'

    def ready(self):
        import BusLinesApp.signals  # noqa