import os
import json
from dotenv import load_dotenv

from agents.Music_preferance_agent import MusicPreferenceAgent
from agents.language_filter import LanguageFilterAgent
from services.spotify_service import SpotifyService
from services.user_spotify_service import UserSpotifyService
from utils.guardrails import validate_recommendations  

def main():
    print(" Starting Music Recommendation Engine...")

    print("🔧 Loading environment variables from .env file...")
    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("OPENAI_API_KEY not found in environment. Exiting.")
        return
    print("OpenAI API Key loaded.")
    print("Initializing Preference & Language agents...")
    preference_agent = MusicPreferenceAgent(openai_api_key)
    language_agent = LanguageFilterAgent(openai_api_key)

    print("🎧 Authenticating Spotify user and initializing services...")
    user_spotify = UserSpotifyService()
    spotify_service = SpotifyService(user_spotify.client)

    # ✅ Take user input
    user_input = input("Enter your music preference : ").strip()
    if not user_input:
        print("No input provided. Exiting.")
        return

    print(f"User input received: '{user_input}'")
    print("Extracting structured preferences from natural language input...")
    preferences = preference_agent.extract_preferences(user_input)
    print(f"Extracted Preferences: {preferences}")

    genre = preferences.get("genre", "pop")
    preferred_language = preferences.get("language", "english")
    print(f"Target Genre: {genre}, Language Preference: {preferred_language}")

    print("Fetching liked song IDs from user's Spotify library...")
    liked_ids = user_spotify.get_all_liked_song_ids()
    print(f"Retrieved {len(liked_ids)} liked song IDs.")

    # Search Spotify for tracks based on preference
    print(f"Searching Spotify for 25 English tracks in genre: {genre}")
    eng_tracks = spotify_service.search_tracks(genre + " english", limit=25)
    print(f"Retrieved {len(eng_tracks)} English tracks.")

    print(f"Searching Spotify for 25 Hindi tracks in genre: {genre}")
    hindi_tracks = spotify_service.search_tracks(genre + " hindi", limit=25)
    print(f" Retrieved {len(hindi_tracks)} Hindi tracks.")
    combined_tracks = eng_tracks + hindi_tracks
    print(f"🔗Combining tracks = {len(combined_tracks)} total tracks.")

    print("Filtering out tracks already liked by the user...")
    filtered_tracks = [track for track in combined_tracks if track["id"] not in liked_ids]
    print(f"{len(filtered_tracks)} tracks remaining after removing liked songs.")
    print(" Cleaning and normalizing track metadata before validation...")
    for track in filtered_tracks:
        track["explicit"] = bool(str(track.get("explicit", False)).lower() == "true")
    print(" Validating track structure using custom validator...")
    validated = validate_recommendations({"recommendations": filtered_tracks})
    if validated["validation_passed"]:
        final_tracks = validated["validated_output"]["recommendations"]
        print(f"Validation passed: {len(final_tracks)} tracks are structurally valid.")
    else:
        print("❌ Validation failed. Exiting.")
        return

    print("\n🎵 Recommendations Before Language Filtering:")
    for i, track in enumerate(final_tracks, 1):
        print(f"{i}. {track['name']} by {track['artist']} (explicit={track['explicit']})")

    print(f"\n Filtering tracks by preferred language: {preferred_language.title()}...")
    language_filtered = language_agent.filter_by_language(final_tracks, preferred_language)
    print(f" {len(language_filtered)} tracks match the preferred language.")

    print(f"\nFinal Recommendations in {preferred_language.title()}:")
    for i, track in enumerate(language_filtered, 1):
        print(f"{i}. {track['name']} by {track['artist']} 🎵 {track.get('spotify_url', '🔗 No link')}")

    print("\nRecommendation flow completed successfully.")

if __name__ == "__main__":
    main()
