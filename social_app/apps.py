from django.apps import AppConfig


class SocialAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_app'

    def ready(self):
        import social_app.signals