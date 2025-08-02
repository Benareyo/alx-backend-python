from django.apps import AppConfig

class DjangoChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Django-Chat'  # folder name with dash and uppercase
    label = 'django_chat'  # valid Python label used internally by Django
