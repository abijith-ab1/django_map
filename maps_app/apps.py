from django.apps import AppConfig


class MapsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maps_app'

    def ready(self):
        import maps_app.signals