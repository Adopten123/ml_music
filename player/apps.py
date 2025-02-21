"""apps.py module"""

from django.apps import AppConfig

class PlayerConfig(AppConfig):
    """ player_config class """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'player'
