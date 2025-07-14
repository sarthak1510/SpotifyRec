from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv

from agents.Music_preferance_agent import MusicPreferenceAgent
from agents.language_filter import LanguageFilterAgent
from services.spotify_service import SpotifyService
from services.user_spotify_service import UserSpotifyService
from utils.guardrails import validate_recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
preference_agent = MusicPreferenceAgent(openai_api_key)
language_agent = LanguageFilterAgent(openai_api_key)
user_spotify = UserSpotifyService()
spotify_service = SpotifyService(user_spotify.client)
class UserPrompt(BaseModel):
    prompt: str
  
@app.post("/recommend")
def get_recommendations(data: UserPrompt):
    logs = []  # Collect all steps
    user_input = data.prompt
    logs.append(" Starting Music Recommendation Engine...")
    logs.append("Initializing recomendation & Language agents...")
    logs.append("Connecting to Sarthak's Spotify using OAuth...")
    preferences = preference_agent.extract_preferences(user_input)
    genre = preferences.get("genre", "pop")
    language = preferences.get("language", "english")
    liked_ids = user_spotify.get_all_liked_song_ids()
    logs.append(f" Retrieved {len(liked_ids)} liked track IDs from user's Spotify library.")
    logs.append(f"Finding recomednations based of your spotify profile")
    eng_tracks = spotify_service.search_tracks(genre + " english", limit=25)
    hin_tracks = spotify_service.search_tracks(genre + " hindi", limit=25)
    combined = eng_tracks + hin_tracks
    filtered = [t for t in combined if t["id"] not in liked_ids]
    logs.append(f"{len(filtered)} tracks remaining after filtering liked songs.")
    for t in filtered:
        t["explicit"] = bool(str(t.get("explicit", False)).lower() == "true")

    logs.append("Applying Gaurdrails to validate results.")
    validated = validate_recommendations({"recommendations": filtered})

    if validated["validation_passed"]:
        final = validated["validated_output"]["recommendations"]
        logs.append(f" Gaurdrails passed: {len(final)} tracks are structurally valid.")
    else:
        logs.append("Gaurdrails failed. Returning empty recommendations.")
        return {"logs": logs, "recommendations": []}

    for i, track in enumerate(final, 1):
        logs.append(f"{i}. {track['name']} by {track['artist']} (explicit={track['explicit']})")

    final_filtered = language_agent.filter_by_language(final, language)
    logs.append(f"\nFiltering tracks by preferred language: {language.title()}...")
    logs.append(f"{len(final_filtered)} tracks match the preferred language.")

    logs.append(f"\nFinal Recommendations in {language.title()}:")
    for i, track in enumerate(final_filtered, 1):
        logs.append(f"{i}. {track['name']} by {track['artist']}  {track.get('spotify_url', 'No link')}")

    logs.append("Recommendation flow completed successfully.")

    return {"logs": logs, "recommendations": final_filtered}
