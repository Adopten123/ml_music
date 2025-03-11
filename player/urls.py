"""Urls of player app"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlayerHome.as_view(), name='main'),
    path('genres/<slug:genre_slug>/', views.genres, name='main_genres'),
    path('genres/<slug:genre_slug>/', views.genres_by_slug, name='main_genres_by_slug'),
    path('information/<slug:info_slug>/', views.InformationPage.as_view(), name='info'),
    path('artists/<slug:artist_slug>/', views.ArtistPage.as_view(), name='artist'),
    path('artists/<slug:artist_slug>/<slug:album_slug>', views.AlbumPage.as_view(), name='show_album'),
    path('search/', views.show_search_page, name='open_search_page'),
    path('search-tracks/', views.search, name='search_tracks'),
    path('playlist/<slug:slug>/', views.PlaylistPage.as_view(), name='playlist_detail'),
    path('add_playlist/', views.AddPlaylistView.as_view(), name='add_playlist'),
    path('update_playlist/<slug:slug>/', views.UpdatePlaylistView.as_view(), name='update_playlist'),
    path('playlist/delete/<slug:slug>/', views.DeletePlaylistView.as_view(), name='delete_playlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
