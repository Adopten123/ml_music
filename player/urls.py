"""Urls of player app"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('genres/<slug:genre_slug>/', views.genres, name='main_genres'),
    path('genres/<slug:genre_slug>/', views.genres_by_slug, name='main_genres_by_slug'),
    path('information/<slug:info_slug>/', views.information, name='info'),
    path('artists/<slug:artist_slug>/', views.artist_card, name='artist'),
    path('artists/<slug:artist_slug>/<slug:album_slug>', views.show_album, name='show_album'),
    path('search/', views.show_search_page, name='open_search_page'),
    path('search-tracks/', views.search, name='search_tracks'),
    path('playlist/<slug:slug>/', views.playlist_detail, name='playlist_detail'),
    path('add_playlist/', views.add_playlist, name='add_playlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
