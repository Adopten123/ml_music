"""Module with Context Processors"""
from .models import Playlist

def get_owned_playlists(request):
    """Function to get all playlists owned by current user"""
    return Playlist.objects.filter(owner=request.user)

def get_added_playlists(request):
    """Function to get all playlists added by current user"""
    return Playlist.objects.filter(added_users=request.user)

def user_playlists(request):
    """Function to get all playlists with current user"""
    if request.user.is_authenticated:
        return {
            "owned_playlists": get_owned_playlists(request),
            "added_playlists": get_added_playlists(request),
        }
    return {}
