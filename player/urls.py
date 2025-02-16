from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('genres/<slug:genre_slug>/', views.genres, name='main_genres'),
    path('genres/<slug:genre_slug>/', views.genres_by_slug, name='main_genres_by_slug'),
    path('information/<slug:info_slug>/', views.information, name='info'),
]
