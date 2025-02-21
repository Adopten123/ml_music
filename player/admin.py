"""Module with settings of admin-panel"""

from django.contrib import admin
from .models import Artist, Genre, Track, Album

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Track)
admin.site.register(Album)
