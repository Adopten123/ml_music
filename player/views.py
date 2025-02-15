from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template.loader import render_to_string

# Create your views here.

#main page views
def index(request): #HttpRequest
    return render(request, 'player/index.html')
#genres main page views
def genres(request):
    return HttpResponse(f"<h1>Genres page</h1>")
#genre page
def genres_by_slug(request, genre_slug):
    return HttpResponse(f"<h1>Genres page</h1> <p> Genre: {genre_slug} </p>")

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Page not found</h1>")