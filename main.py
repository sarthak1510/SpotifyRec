from services.spotify_service import SpotifyService
from dotenv import load_dotenv
import os

load_dotenv()

spotify = SpotifyService()
tracks = spotify.search_tracks("pop")

for idx, track in enumerate(tracks, 1):
    print(f"{idx}. {track['name']} by {track['artist']} (explicit={track['explicit']})")
