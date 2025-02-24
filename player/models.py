"""Models of Player"""
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.

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

    def save(self, *args, **kwargs):
        """Function for making slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TrackPublishedManager(models.Manager): # pylint: disable=R0903
    """Class-manager selects published tracks"""
    def get_queryset(self):
        """Function for getting published tracks"""
        return super().get_queryset().filter(is_published=Track.Status.PUBLISHED)

class Track(models.Model):
    """Class of Music Track"""

    class Status(models.IntegerChoices): # pylint: disable=R0901
        """Choices for track status"""
        UNRELEASED = 0, 'Неопубликованный'
        PUBLISHED = 1, 'Опубликованный'


    name = models.CharField(max_length=128) # track-name
    main_author = models.ForeignKey(Artist, on_delete=models.PROTECT) # the main author of track
    featured_authors = models.ManyToManyField(Artist, related_name='featured_artists', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)  # genre of track
    publication_time = models.DateTimeField(default=timezone.now)

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
        return f'{self.name}'

    class Meta: # pylint: disable=R0903
        """Ordering params"""
        ordering = ['id']
        indexes = [
            models.Index(fields=['id']),  # order-by-id
        ]

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

    def save(self, *args, **kwargs):
        """Function for making slug"""
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)