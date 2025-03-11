"""Views File"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from . import data_for_tests
from .forms import PlaylistForm
from .models import Artist, Track, Genre, Album, Playlist

@login_required
def show_search_page(request):
    """Search Page view"""
    return  render(request, 'player/search_page.html')

def genres(request): # pylint: disable=W0613
    """Genres Page view"""
    return HttpResponse("<h1>Genres page</h1>")

def genres_by_slug(request, genre_slug): # pylint: disable=W0613
    """Genre Page view"""
    return HttpResponse(f"<h1>Genres page</h1> <p> Genre: {genre_slug} </p>")

def page_not_found(request, exception): # pylint: disable=W0613
    """Error Page Views"""
    return HttpResponseNotFound("<h1>Page not found</h1>")

class PlayerHome(LoginRequiredMixin, ListView):
    """Player home view class"""
    template_name = 'player/index.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        return Track.published.select_related('main_author', 'genre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        genres_for_index = Genre.objects.prefetch_related(
            Prefetch(
                'track_set',
                queryset=Track.published.select_related('genre', 'main_author'),
                to_attr='published_tracks'
            )
        )
        context['albums'] = Album.objects.select_related('main_author').all()
        context['tracks_by_genre'] = {genre: genre.published_tracks for genre in genres_for_index}
        context['page_obj'] = data_for_tests.get_page_obj(
            self.request,
            Track.published.select_related('main_author', 'genre')
        )

        return context

class InformationPage(LoginRequiredMixin, TemplateView):
    template_name = "player/base.html"

    def get_template_names(self):
        """Dynamic taking info_slug"""
        return [f"player/information/{self.kwargs['info_slug']}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_slug = self.kwargs['info_slug']

        base_title = data_for_tests.get_title_by_infoslug(info_slug)
        context['title'] = f"{base_title} | ML Music"
        context['info_slug'] = info_slug

        return context


class ArtistPage(LoginRequiredMixin, ListView):
    template_name = 'player/artist_card.html'
    context_object_name = 'all_author_tracks'

    def get_queryset(self):
        self.artist = get_object_or_404(Artist, slug=self.kwargs['artist_slug'])
        return (Track.published.filter(
            Q(main_author=self.artist) | Q(featured_authors=self.artist)
        ).distinct().select_related('main_author', 'genre')
          .prefetch_related('featured_authors')
            .order_by('-publication_time'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tracks_for_column'] = self.get_queryset().order_by('-play_count')[:5]

        context['all_author_albums'] = Album.objects.filter(
            main_author=self.artist
        ).prefetch_related('tracks')

        context.update({
            'artist': self.artist,
            'title': f"{self.artist.name} | ML Music",
            'page_obj': data_for_tests.get_page_obj(self.request, self.get_queryset()),
        })

        return context

class AlbumPage(LoginRequiredMixin, ListView):
    template_name = 'player/album_page.html'
    context_object_name = 'tracks_for_column'

    def get_queryset(self):
        self.album = get_object_or_404(
            Album.objects.select_related('main_author').prefetch_related(
                Prefetch(
                    'tracks',
                    queryset=Track.objects.select_related('main_author', 'genre')
                        .prefetch_related('featured_authors')
                        .order_by('id'),
                    to_attr='prefetched_tracks'
                )
            ),
            main_author__slug=self.kwargs['artist_slug'],
            slug=self.kwargs['album_slug']
        )
        return self.album.prefetched_tracks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'album': self.album,
            'title': f"{self.album.name} | ML Music",
            'page_obj': data_for_tests
                            .get_page_obj(self.request, self.get_queryset()),
        })
        return context

class PlaylistPage(LoginRequiredMixin, ListView):
    template_name = 'player/playlist_detail.html'
    context_object_name = 'tracks_for_column'

    def get_queryset(self):
        self.playlist = get_object_or_404(
            Playlist.objects
            .select_related('owner')
            .prefetch_related(
                Prefetch(
                    'tracks',
                    queryset=Track.objects
                        .select_related('main_author')
                        .prefetch_related('featured_authors')
                )
            ),
            slug=self.kwargs['slug']
        )
        return self.playlist.tracks.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlist'] = self.playlist
        context['page_obj'] = (data_for_tests
                                    .get_page_obj(self.request, self.get_queryset()))
        context['title'] = f"{self.playlist.name} | ML Music"
        return context

@login_required
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

class AddPlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'player/add_playlist.html'

    def get_form_kwargs(self):
        """Adding a user in the form of arguments"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Processing a valid form"""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        form.save_m2m()
        messages.success(self.request, 'Плейлист успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Processing invalid form"""
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        """Adding a title to the context"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание плейлиста'
        return context

class UpdatePlaylistView(LoginRequiredMixin, UpdateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'player/add_playlist.html'

    def get_form_kwargs(self):
        """Adding a user in the form of arguments"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Processing a valid form"""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        form.save_m2m()
        messages.success(self.request, 'Плейлист успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Processing invalid form"""
        messages.error(self.request, 'Исправьте ошибки в форме')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        """Adding a title to the context"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание плейлиста'
        return context


class DeletePlaylistView(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = reverse_lazy('main')  # Укажите целевой URL после удаления

    def get(self, request, *args, **kwargs):
        """Блокируем GET-запросы для безопасности"""
        return HttpResponseForbidden("Доступ запрещен")

    def delete(self, request, *args, **kwargs):
        """Обработка DELETE-запроса"""
        self.object = self.get_object()
        if self.object.owner != request.user:
            return HttpResponseForbidden("Вы не можете удалить этот плейлист")

        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Плейлист успешно удален')
        return HttpResponseRedirect(success_url)