import os
from dotenv import load_dotenv
import spotipy 
from spotipy.oauth2 import SpotifyOAuth 

class UserSpotifyService: 
    def __init__(self):
        load_dotenv()

        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

        if not client_id or not client_secret or not redirect_uri:
            raise ValueError("❌ Missing Spotify credentials in environment variables.")

        self.client = spotipy.Spotify(  
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-library-read",
                cache_path=None,
                show_dialog=True
            )
        )

        print("UserSpotifyService initialized with forced fresh login.")

    def get_all_liked_song_ids(self) -> list:
        all_ids = []
        offset = 0
        limit = 50

        while True:
            results = self.client.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get("items", [])
            if not items:
                break

            all_ids.extend(
                item["track"]["id"]
                for item in items
                if item.get("track")
            )
            offset += limit

        print(f"Retrieved {len(all_ids)} total liked track IDs.")
        return all_ids

    def get_all_liked_songs(self) -> list:
        all_songs = []
        offset = 0
        limit = 50

        while True:
            results = self.client.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get("items", [])
            if not items:
                break

            all_songs.extend(
                {
                    "name": item["track"]["name"],
                    "artist": item["track"]["artists"][0]["name"],
                    "id": item["track"]["id"]
                }
                for item in items
                if item.get("track")
            )
            offset += limit

        print(f"Retrieved {len(all_songs)} total liked songs.")
        return all_songs
