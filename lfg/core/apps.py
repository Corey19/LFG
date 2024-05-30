from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    models = [
        'User', 'Tags', 'Groups', 'Games', 'Friend'  # Add your model class here
    ]