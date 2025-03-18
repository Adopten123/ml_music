"""Tests for app"""
import uuid
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from pytils.translit import slugify

from .models import (
    Genre,
    Artist,
    Track,
    Album
)

User = get_user_model()


class ModelTests(TestCase):
    """Tests for app"""
    def setUp(self):
        self.genre = Genre.objects.create(name=f"Rock {uuid.uuid4().hex[:6]}")

        artist_name = f"Test Artist {uuid.uuid4().hex[:6]}"
        self.artist = Artist.objects.create(
            name=artist_name,
            genre=self.genre,
            logo=SimpleUploadedFile("artist.jpg", b"fakeimagecontent")
        )

        with patch('mutagen.mp3.MP3') as mock_mp3:
            mock_mp3.return_value.info.length = 180  # 3 минуты
            self.track = Track.objects.create(
                name='Test Track',
                main_author=self.artist,
                genre=self.genre,
                mp3=SimpleUploadedFile("tracks/Intro.mp3", b"\x00\x01\x02"),
                logo=SimpleUploadedFile("track.jpg", b"fakeimagecontent")
            )

        self.album = Album.objects.create(
            name=f"Test Album {uuid.uuid4().hex[:6]}",
            main_author=self.artist,
            genre=self.genre,
            logo=SimpleUploadedFile("album.jpg", b"fakeimagecontent")
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_genre_creation(self):
        """Tests genre creation"""
        self.assertEqual(self.genre.slug, slugify(self.genre.name))
        self.assertEqual(str(self.genre), self.genre.name)

    def test_artist_slug_creation(self):
        """Tests artist slug creation"""
        new_name = uuid.uuid4().hex[:16]
        artist = Artist.objects.create(
            name=new_name,
            slug=slugify(new_name),
            genre=self.genre,
            logo=SimpleUploadedFile("artist.jpg", b"fakeimagecontent")
        )
        self.assertEqual(artist.slug, slugify(new_name))

    def test_album_tracks_relationship(self):
        """Tests album tracks relationship"""
        self.album.tracks.add(self.track)
        self.assertIn(self.track, self.album.tracks.all())


class ViewTests(TestCase):
    """View tests"""
    def setUp(self):
        """Set up data for test"""
        self.client = Client()
        self.genre = Genre.objects.create(name=f"Rock {uuid.uuid4().hex[:6]}")

        artist_name = f"Test Artist {uuid.uuid4().hex[:6]}"
        self.artist = Artist.objects.create(
            name=artist_name,
            genre=self.genre,
            slug=slugify(artist_name),
            logo=SimpleUploadedFile("artist.jpg", b"fakeimagecontent")
        )

        self.track = Track.objects.create(
            name='Test Track',
            main_author=self.artist,
            genre=self.genre,
            mp3=SimpleUploadedFile("test.mp3", b"\x00\x01\x02"),
            logo=SimpleUploadedFile("track.jpg", b"fakeimagecontent")
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_main_page_auth_required(self):
        """Tests main page auth required"""
        response = self.client.get(reverse('main'))
        self.assertRedirects(response, '/login/?next=/', 302)

    def test_artist_page(self):
        """Tests artist page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('artist', kwargs={'artist_slug': self.artist.slug}))
        self.assertEqual(response.status_code, 200)

    def test_album_page(self):
        """Tests album page"""
        new_name = f"Test Album {uuid.uuid4().hex[:6]}"
        album = Album.objects.create(
            name=new_name,
            main_author=self.artist,
            genre=self.genre,
            slug=slugify(new_name),
            logo=SimpleUploadedFile("album.jpg", b"fakeimagecontent")
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('show_album',
                    kwargs={'artist_slug': self.artist.slug, 'album_slug': album.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_search_functionality(self):
        """Tests search functionality"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('search_tracks'), {'query': 'Test'})
        self.assertContains(response, self.track.name)


class AdminTests(TestCase):
    """Tests for admin"""
    def setUp(self):
        """Set up data for test"""
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.genre = Genre.objects.create(name=f"Rock {uuid.uuid4().hex[:6]}")

        self.artist = Artist.objects.create(
            name=f"Test Artist {uuid.uuid4().hex[:6]}",
            genre=self.genre,
            logo=SimpleUploadedFile("artist.jpg", b"fakeimagecontent")
        )

    def test_track_admin_actions(self):
        """Tests admin actions"""
        track = Track.objects.create(
            name='Test Track',
            main_author=self.artist,
            genre=self.genre,
            is_published=Track.Status.UNRELEASED,
            mp3=SimpleUploadedFile("test.mp3", b"\x00\x01\x02")
        )
        self.client.login(username='admin', password='adminpass')
        self.client.post(
            reverse('admin:player_track_changelist'),
            {'action': 'set_published', '_selected_action': [track.id]},
            follow=True
        )
        track.refresh_from_db()
        self.assertEqual(track.is_published, Track.Status.PUBLISHED)

    def test_artist_admin_interface(self):
        """Tests admin interface"""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('admin:player_artist_changelist'))
        self.assertContains(response, self.artist.name)


class ErrorHandlingTests(TestCase):
    """Tests for error handling"""
    def test_404_page(self):
        """Tests 404 page"""
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
