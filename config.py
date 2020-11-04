import spotipy
from spotipy.oauth2 import SpotifyOAuth

#config
scope = "user-library-read,user-read-playback-state,user-modify-playback-state,user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
