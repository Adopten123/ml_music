"""Views File"""
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Prefetch

from . import data_for_tests
from .models import Artist, Track, Genre, Album

def index(request):
    """Main Page view"""

    # Загружаем жанры с предзагрузкой связанных треков
    genres = Genre.objects.prefetch_related(
        Prefetch(
            'track_set',
            queryset=Track.published.select_related('genre', 'main_author'),
            to_attr='published_tracks'
        )
    )

    albums = Album.objects.select_related('main_author').all()

    tracks_by_genre = {genre: genre.published_tracks for genre in genres}

    data = {
        'albums': albums,
        'tracks_by_genre': tracks_by_genre,
        'page_obj': data_for_tests.get_page_obj(request, Track.published.select_related('main_author', 'genre')),
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

    all_author_tracks = Track.published.filter(
        Q(main_author=artist) | Q(featured_authors=artist)
    ).distinct().select_related('main_author', 'genre').prefetch_related('featured_authors') \
     .order_by('-publication_time')

    top5_tracks = all_author_tracks.order_by('-play_count')[:5]

    all_author_albums = Album.objects.filter(main_author=artist).prefetch_related('tracks')

    data = {
        'artist': artist,
        'title': artist.name + ' | ML Music',
        'tracks_for_column': top5_tracks,
        'all_author_tracks': all_author_tracks,
        'all_author_albums': all_author_albums,
        'page_obj': data_for_tests.get_page_obj(request, all_author_tracks),
    }

    return render(request, 'player/artist_card.html', data)

def show_album(request, artist_slug, album_slug):
    """Album Page view"""
    album = get_object_or_404(
        Album.objects.select_related('main_author').prefetch_related(
            Prefetch(
                'tracks',
                queryset=Track.objects.select_related('main_author', 'genre')
                    .prefetch_related('featured_authors')
                    .order_by('id'),
                to_attr='prefetched_tracks'
            )
        ),
        main_author__slug=artist_slug,
        slug=album_slug
    )

    tracks = album.prefetched_tracks

    data = {
        'album': album,
        'title': album.name + ' | ML Music',
        'tracks_for_column': tracks,
        'page_obj': data_for_tests.get_page_obj(request, tracks),
    }
    return render(request, 'player/album_page.html', data)

def show_search_page(request):
    return render(request, 'player/search_page.html')

def search(request):
    """Search Page view"""
    query = request.GET.get('query', '').strip()

    if query:
        tracks = Track.objects.select_related('main_author').filter(
            Q(name__icontains=query) | Q(main_author__name__icontains=query)
        ).order_by('id')
    else:
        tracks = Track.objects.none()

    context = {
        'tracks': tracks,
        'title': 'Search | ML Music',
        'marker': 'search_page',
        'page_obj': data_for_tests.get_page_obj(request, tracks),
    }

    return render(request, 'player/search_page.html', context)


def page_not_found(request, exception): # pylint: disable=W0613
    """Error Page Views"""
    return HttpResponseNotFound("<h1>Page not found</h1>")

