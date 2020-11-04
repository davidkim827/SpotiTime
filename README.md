# SpotiTime
Plays playlists according to a time schedule:
This script was born out of my wanting to make Christmas perfect by playing more upbeat songs during the day and instrumental Christmas music at night automatically.
Sort of messy, but wanted a quick and dirty solution.


A CLI to set a user's spotify application to play certain playlists according to a time schedule a user sets.

This script requires you to create a developer account with Spotify to grab the following env vars and set them:

$env:SPOTIPY_CLIENT_ID = "CLIENT ID"
$env:SPOTIPY_CLIENT_SECRET = "CLIENT_SECRET"
$env:SPOTIPY_REDIRECT_URI = "REDIRECT_URI"
