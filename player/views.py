from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from . import data_for_tests
from .models import Artist


# Create your views here.


#main page views
def index(request):
    data = {
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

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Page not found</h1>")

def artist_card(request, artist_slug):
    queryset = Artist.objects.filter(slug=artist_slug)

    if not queryset.exists():
        return page_not_found(request, artist_slug)

    data = {
        'artist': queryset.first(),
    }
    return render(request, 'player/artist_card.html', data)