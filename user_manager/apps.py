"""apps.py module"""

from django.apps import AppConfig


class UserManagerConfig(AppConfig):
    """user manager app config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_manager"
