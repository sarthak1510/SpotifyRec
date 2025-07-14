class SpotifyService:
    def __init__(self, client):
        self.client = client

    def search_tracks(self, query, limit=10):
        """
        Search for tracks on Spotify given a query string.
        Ensures all returned tracks have the required metadata.
        """
        results = self.client.search(q=query, type="track", limit=limit)
        tracks = []

        for item in results['tracks']['items']:
            track_id = item.get('id')
            name = item.get('name')
            artist = item['artists'][0]['name'] if item.get('artists') else "Unknown"
            explicit = item.get('explicit', False)
            spotify_url = item.get('external_urls', {}).get('spotify', '') 

            if track_id and name:
                tracks.append({
                    "id": track_id,
                    "name": name,
                    "artist": artist,
                    "explicit": explicit,
                    "spotify_url": spotify_url  
                })

        return tracks
