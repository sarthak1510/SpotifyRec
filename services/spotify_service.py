from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyService:
    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
        self.client = Spotify(auth_manager=auth)

    def search_tracks(self, query="pop", limit=5):
        results = self.client.search(q=query, type="track", limit=limit)
        tracks = []
        for t in results["tracks"]["items"]:
            tracks.append({
                "name": t["name"],
                "artist": t["artists"][0]["name"],
                "explicit": t["explicit"]
            })
        return tracks
