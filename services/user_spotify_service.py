import os
import json
import time
import spotipy
import requests
from requests.auth import HTTPBasicAuth

class UserSpotifyService:
    def __init__(self):
        # Get token JSON and credentials from environment
        token_raw = os.getenv("SPOTIFY_TOKEN_JSON")
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

        if not token_raw or not client_id or not client_secret:
            raise ValueError("❌ Missing Spotify credentials or token JSON in environment.")

        self.token_info = json.loads(token_raw)

        # Refresh token if expired
        if self.token_info["expires_at"] < int(time.time()):
            self.refresh_token(client_id, client_secret)

        self.client = spotipy.Spotify(auth=self.token_info["access_token"])
        print("✅ Spotify client initialized with existing token.")

    def refresh_token(self, client_id, client_secret):
        refresh_token = self.token_info["refresh_token"]

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            },
            auth=HTTPBasicAuth(client_id, client_secret)
        )

        if response.status_code != 200:
            raise Exception(f"❌ Failed to refresh token: {response.text}")

        new_token = response.json()
        self.token_info["access_token"] = new_token["access_token"]
        self.token_info["expires_at"] = int(time.time()) + new_token["expires_in"]

        self.client = spotipy.Spotify(auth=self.token_info["access_token"])
        print("🔁 Spotify token refreshed.")

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

        print(f"🎵 Retrieved {len(all_ids)} total liked track IDs.")
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

            all_songs.extend(
                {
                    "name": item["track"]["name"],
                    "artist": item["track"]["artists"][0]["name"],
                    "id": item["track"]["id"]
                }
                for item in items if item.get("track")
            )
            offset += limit

        print(f"🎶 Retrieved {len(all_songs)} liked songs.")
        return all_songs
