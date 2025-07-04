from dotenv import load_dotenv
import os

from agents.Music_preferance_agent import MusicPreferenceAgent

from services.spotify_service import SpotifyService


def main():
    # load environment
    load_dotenv()
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ Please set OPENAI_API_KEY in your .env")
        return

    # init agent
    agent = MusicPreferenceAgent(openai_api_key)

    # init spotify
    spotify = SpotifyService()

    # get user input
    user_input = input("🎤 Enter your music preference: ")

    # extract preferences
    preferences = agent.extract_preferences(user_input)
    print(f"✅ Preferences extracted: {preferences}")

    # search using genre from preferences
    genre = preferences.get("genre", "pop")
    tracks = spotify.search_tracks(genre)

    # display tracks
    if not tracks:
        print("❌ No tracks found.")
        return

    for idx, track in enumerate(tracks, 1):
        print(f"{idx}. {track['name']} by {track['artist']} (explicit={track['explicit']})")

if __name__ == "__main__":
    main()
