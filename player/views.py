from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string

from . import data_for_tests
from .models import Artist, Track, Genre, Album


# Create your views here.


#main page views
def index(request):
    paginator = Paginator(Track.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    genres = Genre.objects.all()
    tracks_by_genre = {genre: Track.objects.filter(genre=genre, is_published=Track.Status.PUBLISHED) for genre
                       in genres}
    albums = Album.objects.all()

    data = {
        'albums': albums,
        'tracks_by_genre': tracks_by_genre,
        'page_obj': page_obj,
    }#HttpRequest
    return render(request, 'player/index.html', data)
#genres main page views
def genres(request):
    return HttpResponse(f"<h1>Genres page</h1>")
#genre page
def genres_by_slug(request, genre_slug):
    return HttpResponse(f"<h1>Genres page</h1> <p> Genre: {genre_slug} </p>")
#lower menu information pages
def information(request, info_slug):

    title_to_find = data_for_tests.get_title_by_infoslug(info_slug) + ' | ML Music'

    data = {
        'title': title_to_find,
        'info_slug': info_slug
    }
    return render(request, f"player/information/{info_slug}.html", data)

def artist_card(request, artist_slug):
    artist = get_object_or_404(Artist, slug=artist_slug)

    data = {
        'artist': artist,
    }
    return render(request, 'player/artist_card.html', data)

def show_album(request, artist_slug, album_slug):
    album = get_object_or_404(Album, main_author__slug=artist_slug, slug=album_slug)
    tracks = album.tracks.all()

    paginator = Paginator(tracks, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'album': album,
        'tracks': tracks,
        'page_obj': page_obj,
    }
    return render(request, 'player/album_page.html', data)

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Page not found</h1>")