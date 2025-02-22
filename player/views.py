"""Views File"""
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound

from . import data_for_tests
from .models import Artist, Track, Genre, Album

def index(request):
    """Main Page view"""

    genres_arr = Genre.objects.all()
    tracks_by_genre = {genre: Track.objects
        .filter(genre=genre, is_published=Track.Status.PUBLISHED) for genre in genres_arr}
    albums = Album.objects.all()

    data = {
        'albums': albums,
        'tracks_by_genre': tracks_by_genre,
        'page_obj': data_for_tests.get_page_obj(request, Track.published.all()),
    }
    return render(request, 'player/index.html', data)

def genres(request): # pylint: disable=W0613
    """Genres Page view"""
    return HttpResponse("<h1>Genres page</h1>")

def genres_by_slug(request, genre_slug): # pylint: disable=W0613
    """Genre Page view"""
    return HttpResponse(f"<h1>Genres page</h1> <p> Genre: {genre_slug} </p>")

def information(request, info_slug):
    """Information Page view"""
    title_to_find = data_for_tests.get_title_by_infoslug(info_slug) + ' | ML Music'

    data = {
        'title': title_to_find,
        'info_slug': info_slug
    }
    return render(request, f"player/information/{info_slug}.html", data)

def artist_card(request, artist_slug):
    """Artists Page view"""
    artist = get_object_or_404(Artist, slug=artist_slug)

    top5_tracks = Track.published.filter(main_author=artist).order_by('-play_count')[:5]

    data = {
        'artist': artist,
        'top5_tracks': top5_tracks,
        'page_obj': data_for_tests.get_page_obj(request, Track.published.all()),
    }
    return render(request, 'player/artist_card.html', data)

def show_album(request, artist_slug, album_slug):
    """Album Page view"""
    album = get_object_or_404(Album, main_author__slug=artist_slug, slug=album_slug)
    tracks = album.tracks.all()

    data = {
        'album': album,
        'tracks': tracks,
        'page_obj': data_for_tests.get_page_obj(request, tracks),
    }
    return render(request, 'player/album_page.html', data)

def show_search_page(request):
    return render(request, 'player/search_page.html')

def search(request):
    """Search Page view"""
    query = request.GET.get('query', '').strip()

    tracks = Track.objects.filter(name__icontains=query) | Track.objects.filter(main_author__name__icontains=query)

    context = {
        'tracks': tracks,
        'marker': 'search_page',
        'page_obj': data_for_tests.get_page_obj(request, tracks),
    }

    return render(request, 'player/search_page.html', context)

def page_not_found(request, exception): # pylint: disable=W0613
    """Error Page Views"""
    return HttpResponseNotFound("<h1>Page not found</h1>")

