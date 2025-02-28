from .models import Playlist

def get_owned_playlists(request):
    return Playlist.objects.filter(owner=request.user)

def get_added_playlists(request):
    return Playlist.objects.filter(added_users=request.user)

def user_playlists(request):
    if request.user.is_authenticated:
        return {
            "owned_playlists": get_owned_playlists(request),
            "added_playlists": get_added_playlists(request),
        }
    return {}