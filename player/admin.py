"""Module with settings of admin-panel"""

from django.contrib import admin
from .models import Artist, Genre, Track, Album, Playlist

#rename admin-panel
admin.site.site_header = "ML Music admin-panel"

class TrackAdmin(admin.ModelAdmin):
    """class for changing viewing of tracks in admin panel"""
    filter_horizontal = ['featured_authors']

    exclude = ['duration', 'play_count']

    list_display = ('id', 'name', 'main_author', 'publication_time', 'is_published')
    list_display_links = ('id', 'name')
    list_filter = ('is_published', 'genre__name')
    list_per_page = 20
    ordering = ['-publication_time', '-name']
    search_fields = ['name', 'main_author__name']

    actions = ['set_published', 'set_unreleased']

    @admin.action(description="Make published status")
    def set_published(self, request, queryset): # pylint: disable=W0613
        """Action for setting published status in admin panel"""
        queryset.update(is_published = Track.Status.PUBLISHED)

    @admin.action(description="Make unreleased status")
    def set_unreleased(self, request, queryset): # pylint: disable=W0613
        """Action for setting unpublished status in admin panel"""
        queryset.update(is_published=Track.Status.UNRELEASED)

class GenreAdmin(admin.ModelAdmin):
    """class for changing viewing of genres in admin panel"""
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    list_per_page = 20
    ordering = ['id', 'name']
    readonly_fields = ['slug',]

class ArtistAdmin(admin.ModelAdmin):
    """class for changing viewing of artists in admin panel"""
    list_display = ('id', 'name', 'slug', 'is_confirmed')
    list_display_links = ('id', 'name', 'slug')
    list_filter = ('is_confirmed', 'genre__name')
    list_per_page = 20
    ordering = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    actions = ['set_confirmed', 'set_unconfirmed']

    @admin.action(description="Make confirmed status")
    def set_confirmed(self, request, queryset): # pylint: disable=W0613
        """Action for setting confirmed status in admin panel"""
        queryset.update(is_published=Artist.Status.CONFIRMED)

    @admin.action(description="Make unconfirmed status")
    def set_unconfirmed(self, request, queryset): # pylint: disable=W0613
        """Action for setting unconfirmed status in admin panel"""
        queryset.update(is_published=Artist.Status.UNCONFIRMED)



class AlbumAdmin(admin.ModelAdmin):
    """class for changing viewing of albums in admin panel"""
    filter_horizontal = ['tracks']
    list_display = ('id', 'name', 'main_author', 'publication_time', 'is_published')
    list_display_links = ('id', 'name')
    list_filter = ('is_published', 'genre__name')
    list_per_page = 20
    ordering = ['-publication_time', '-name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'main_author__name']

    actions = ['set_published', 'set_unreleased']

    @admin.action(description="Make published status")
    def set_published(self, request, queryset): # pylint: disable=W0613
        """Action for setting published status in admin panel"""
        queryset.update(is_published=Album.Status.PUBLISHED)

    @admin.action(description="Make unreleased status")
    def set_unreleased(self, request, queryset): # pylint: disable=W0613
        """Action for setting unpublished status in admin panel"""
        queryset.update(is_published=Album.Status.UNRELEASED)

class PlaylistAdmin(admin.ModelAdmin):
    """class for changing viewing of playlist in admin panel"""
    filter_horizontal = ['tracks']
    list_display = ('id', 'name', 'owner', 'time_created', 'is_public')
    list_display_links = ('id', 'name')
    list_filter = ('is_public', 'owner__username')
    list_per_page = 20
    ordering = ['-time_created', '-name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'owner__username']

    actions = ['set_published', 'set_unreleased']

    @admin.action(description="Make published status")
    def set_published(self, request, queryset):  # pylint: disable=W0613
        """Action for setting public status in admin panel"""
        queryset.update(is_published=Playlist.Status.PUBLIC)

    @admin.action(description="Make unreleased status")
    def set_unreleased(self, request, queryset):  # pylint: disable=W0613
        """Action for setting private status in admin panel"""
        queryset.update(is_published=Playlist.Status.PRIVATE)

admin.site.register(Track, TrackAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Playlist, PlaylistAdmin)
