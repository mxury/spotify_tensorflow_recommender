from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def create_upload_playlist(pl_name, track_ids):
    """
    Creates a new playlist with name 'pl_name', populating it with tracks whose id's reside in 'track_ids'
    :param pl_name: (str) Name of the playlist to be created
    :param track_ids: (list) List of track ids
    :return: None
    """
    load_dotenv()
    scope = 'playlist-modify-public'
    sp_private = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    user_id = 'kv718oiku8q612q0zi4iaovzb'
    result = sp_private.user_playlist_create(user_id, pl_name)

    playlist_id = result['id']
    sp_private.playlist_add_items(playlist_id, track_ids)
    return



