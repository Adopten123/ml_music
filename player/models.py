from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.

#Class of Music Genre
class Genre(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=256, unique=True)

    def __str__(self):
        return self.name

#Class-manager selects confirmed performers
class ConfirmedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_confirmed=True)

#Class of Music Artist
class Artist(models.Model):
    name = models.CharField(max_length=64) # artist name
    slug = models.SlugField(max_length=64, unique=True) # artist slug for artist page
    logo = models.ImageField(upload_to='artists/',blank=False, null=True) # logo of artist
    is_confirmed = models.BooleanField(default=False)
    sub_count = models.IntegerField(default=0)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT) # the main genre of artist

    # Models Managers
    objects = models.Manager()
    confirmed = ConfirmedManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artists', kwargs={'slug': self.slug})

#Class-manager selects published tracks
class TrackPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Track.STATUS.PUBLISHED)

class Track(models.Model):

    class Status(models.IntegerChoices):
        UNRELEASED = 0, 'НЕОПУБЛИКОВАННЫЙ'
        PUBLISHED = 1, 'ОПУБЛИКОВАННЫЙ'


    name = models.CharField(max_length=128) # track-name
    main_author = models.ForeignKey(Artist, on_delete=models.PROTECT) # the main author of track
    featured_authors = models.ManyToManyField(Artist, related_name='featured_artists', blank=True)  # the featured artists
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)  # genre of track
    publication_time = models.DateTimeField(default=timezone.now)

    #Moderator Info
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    logo = models.ImageField(upload_to=f"tracks_logo/", blank=False, null=True) # logo of track
    mp3 = models.FileField(upload_to=f"tracks/", blank=False, null=True) # mp3 of track
    lyrics = models.TextField(blank=True, null=True)
    duration = models.CharField(default=0, max_length=32)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)  # status публикации трека

    # Models Managers
    objects = models.Manager()
    published = TrackPublishedManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['id']),  # order-by-id
        ]

#Class-manager selects published albums
class AlbumPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Album.STATUS.PUBLISHED)

class Album(models.Model):

    class Status(models.IntegerChoices):
        UNRELEASED = 0, 'НЕОПУБЛИКОВАННЫЙ'
        PUBLISHED = 1, 'ОПУБЛИКОВАННЫЙ'

    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=64, blank=True)
    main_author = models.ForeignKey(Artist, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    tracks = models.ManyToManyField(Track, related_name='albums', blank=True)
    publication_time = models.DateTimeField(default=timezone.now)

    # Moderator Info
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    logo = models.ImageField(upload_to=f"playlists/", blank=False, null=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED)

    # Models Managers
    objects = models.Manager()
    published = AlbumPublishedManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created']),  # order-by-time-of-publication
        ]