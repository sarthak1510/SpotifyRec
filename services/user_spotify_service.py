import os
import time
import spotipy
import requests
from requests.auth import HTTPBasicAuth


class UserSpotifyService:
    def __init__(self):
        self.access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")
        self.expires_at = int(os.getenv("SPOTIFY_EXPIRES_AT", "0"))
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

        if not all([self.access_token, self.refresh_token, self.client_id, self.client_secret]):
            raise ValueError("❌ Missing one or more Spotify credentials.")

        # Refresh token if expired
        if self.expires_at < int(time.time()):
            print("🔄 Access token expired. Refreshing...")
            self.refresh_token_func()

        self.client = spotipy.Spotify(auth=self.access_token)
        print("✅ Spotify client initialized with access token.")

    def refresh_token_func(self):
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            },
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )

        if response.status_code != 200:
            raise Exception(f"❌ Failed to refresh token: {response.text}")

        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.expires_at = int(time.time()) + token_data["expires_in"]

        # ⚠️ You must update Render’s env vars manually if needed.
        print("🔁 Refreshed token. NOTE: Set new env vars if needed for persistence.")

        self.client = spotipy.Spotify(auth=self.access_token)

    def get_all_liked_song_ids(self):
        all_ids = []
        offset = 0
        limit = 50

        while True:
            results = self.client.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get("items", [])
            if not items:
                break

            all_ids.extend(item["track"]["id"] for item in items if item.get("track"))
            offset += limit

        print(f"🎵 Retrieved {len(all_ids)} liked song IDs.")
        return all_ids

    def get_all_liked_songs(self):
        all_songs = []
        offset = 0
        limit = 50

        while True:
            results = self.client.current_user_saved_tracks(limit=limit, offset=offset)
            items = results.get("items", [])
            if not items:
                break

            all_songs.extend({
                "name": item["track"]["name"],
                "artist": item["track"]["artists"][0]["name"],
                "id": item["track"]["id"]
            } for item in items if item.get("track"))

            offset += limit

        print(f"🎶 Retrieved {len(all_songs)} liked songs.")
        return all_songs
