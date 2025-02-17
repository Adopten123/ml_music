from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Artist

admin.site.register(Artist)