"""Models of Player"""
import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify
from mutagen.mp3 import MP3


class PlayerUser(AbstractUser):
    """Player User Class"""
    profile_photo = models.ImageField(upload_to='profile_logo', blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

class Genre(models.Model):
    """Class of Music Genre"""
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)

    # Models Managers
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        """Function for making slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ConfirmedManager(models.Manager): # pylint: disable=R0903
    """Class-manager selects confirmed performers"""
    def get_queryset(self):
        """Function for getting confirmed authors"""
        return super().get_queryset().filter(is_confirmed=True)

class Artist(models.Model):
    """Class of Music Artist"""

    class Status(models.IntegerChoices): # pylint: disable=R0901
        """Confirmed status of Artist"""
        UNCONFIRMED = 0, 'Неподтвержденный'
        CONFIRMED = 1, 'Подтвержденный'

    name = models.CharField(max_length=64) # artist name
    slug = models.SlugField(max_length=64, unique=True) # artist slug for artist page
    logo = models.ImageField(upload_to='artists/',blank=False, null=True) # logo of artist
    is_confirmed = models.BooleanField(choices=Status.choices, default=Status.CONFIRMED)
    sub_count = models.IntegerField(default=0)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT) # the main genre of artist

    # Models Managers
    objects = models.Manager()
    confirmed = ConfirmedManager()

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """return url for artist page"""
        return reverse('artist', kwargs={'artist_slug': self.slug})

class TrackPublishedManager(models.Manager): # pylint: disable=R0903
    """Class-manager selects published tracks"""
    def get_queryset(self):
        """Function for getting published tracks"""
        return super().get_queryset().filter(is_published=Track.Status.PUBLISHED)

class Track(models.Model):
    """Class of Music Track"""

    def default_publication_time(): # pylint: disable=E0211
        """Return time with params 00:00:00"""
        return timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)

    class Status(models.IntegerChoices): # pylint: disable=R0901
        """Choices for track status"""
        UNRELEASED = 0, 'Неопубликованный'
        PUBLISHED = 1, 'Опубликованный'


    name = models.CharField(max_length=128) # track-name
    main_author = models.ForeignKey(Artist, on_delete=models.PROTECT) # the main author of track
    featured_authors = models.ManyToManyField(Artist, related_name='featured_artists', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)  # genre of track
    publication_time = models.DateTimeField(default=default_publication_time)

    #Moderator Info
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    logo = models.ImageField(upload_to="tracks_logo/", blank=False, null=True) # logo of track
    mp3 = models.FileField(upload_to="tracks/", blank=False, null=True) # mp3 of track
    lyrics = models.TextField(blank=True, null=True)
    duration = models.CharField(default=0, max_length=32)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)

    play_count = models.IntegerField(default=0)

    # Models Managers
    objects = models.Manager()
    published = TrackPublishedManager()

    def __str__(self):
        return f"{self.name} - {self.main_author}"

    class Meta: # pylint: disable=R0903
        """Ordering params"""
        ordering = ['id']
        indexes = [
            models.Index(fields=['id']),  # order-by-id
        ]

    def save(self, *args, **kwargs):
        """Auto compute of track duration"""
        if self.mp3:
            mp3_path = self.mp3.path # pylint: disable=no-member
            if os.path.exists(mp3_path):
                audio = MP3(mp3_path)
                duration_seconds = int(audio.info.length)

                hours, remainder = divmod(duration_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                if hours:
                    self.duration = f"{hours}.{minutes:02}.{seconds:02}"
                else:
                    self.duration = f"{minutes}.{seconds:02}"

        super().save(*args, **kwargs)

class AlbumPublishedManager(models.Manager): # pylint: disable=R0903
    """Class-manager selects published albums"""
    def get_queryset(self):
        """Function for getting published albums"""
        return super().get_queryset().filter(is_published=Album.Status.PUBLISHED)

class Album(models.Model):
    """Class of Music Album"""
    class Status(models.IntegerChoices): # pylint: disable=R0901
        """Choices for album status"""
        UNRELEASED = 0, 'Неопубликованный'
        PUBLISHED = 1, 'Опубликованный'

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, blank=True)
    main_author = models.ForeignKey(Artist, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    tracks = models.ManyToManyField(Track, related_name='albums', blank=True)
    publication_time = models.DateTimeField(default=timezone.now)

    # Moderator Info
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    logo = models.ImageField(upload_to="playlists/", blank=False, null=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)

    # Models Managers
    objects = models.Manager()
    published = AlbumPublishedManager()

    def __str__(self):
        return f'{self.name}'

    class Meta: # pylint: disable=R0903
        """Ordering params"""
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created']),  # order-by-time-of-publication
        ]

class PlayListPublicManager(models.Manager): # pylint: disable=R0903
    """Class-manager selects public playlists"""
    def get_queryset(self):
        """Function for getting published albums"""
        return super().get_queryset().filter(is_published=Playlist.Status.PUBLIC)

class Playlist(models.Model):
    """Class of Music Playlist"""
    class Status(models.IntegerChoices): # pylint: disable=R0901
        """Choices for playlist status"""
        PRIVATE = 0, "Приватный"
        PUBLIC = 1, "Публичный"

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, unique=True, blank=True)

    owner = models.ForeignKey(PlayerUser, on_delete=models.PROTECT)
    added_users = models.ManyToManyField(PlayerUser, related_name='friends', blank=True)
    tracks = models.ManyToManyField(Track, related_name='playlists', blank=True)

    logo = models.ImageField(upload_to="playlists/", blank=False, null=True)
    is_public = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices))
                                    , default=Status.PUBLIC)

    # Moderator Info
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    # Models Managers
    objects = models.Manager()
    public = PlayListPublicManager()

    def __str__(self):
        return f'{self.name} of {self.owner}'

    def get_absolute_url(self):
        """return url for playlist page"""
        return reverse('playlist_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """Function for making slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
