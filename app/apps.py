from django.apps import AppConfig as DjangoAppConfiga


class AppConfig(DjangoAppConfiga):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self) -> None:
        import app.signals
