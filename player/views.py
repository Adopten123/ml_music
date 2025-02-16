from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from . import data_for_tests
# Create your views here.


#main page views
def index(request):
    data = {
        'title': 'ML Music',
        'lowermenu_buttons': data_for_tests.lowermenu_buttons,
    }#HttpRequest
    return render(request, 'player/index.html', data)
#genres main page views
def genres(request):
    return HttpResponse(f"<h1>Genres page</h1>")
#genre page
def genres_by_slug(request, genre_slug):
    return HttpResponse(f"<h1>Genres page</h1> <p> Genre: {genre_slug} </p>")

def information(request, info_slug):
    data = {
        'title': 'ML Music',
        'lowermenu_buttons': data_for_tests.lowermenu_buttons,
        'info_slug': info_slug
    }
    return render(request, f"player/information/{info_slug}.html", data)

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Page not found</h1>")