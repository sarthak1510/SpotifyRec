from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from agents.Music_preferance_agent import MusicPreferenceAgent
from agents.language_filter import LanguageFilterAgent
from services.spotify_service import SpotifyService
from services.user_spotify_service import UserSpotifyService
from utils.guardrails import validate_recommendations

# Setup
load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_api_key = os.getenv("OPENAI_API_KEY")
preference_agent = MusicPreferenceAgent(openai_api_key)
language_agent = LanguageFilterAgent(openai_api_key)
user_spotify = UserSpotifyService()
spotify_service = SpotifyService(user_spotify.client)

# Models
class UserPrompt(BaseModel):
    prompt: str

# Endpoints
@app.get("/")
def root():
    return {"message": "Spotify Recommendation API is running 🚀"}

@app.post("/recommend")
def get_recommendations(data: UserPrompt):
    logs = []
    user_input = data.prompt
    logs.append("Starting Music Recommendation Engine...")

    preferences = preference_agent.extract_preferences(user_input)
    genre = preferences.get("genre", "pop")
    language = preferences.get("language", "english")

    liked_ids = user_spotify.get_all_liked_song_ids()
    logs.append(f"Retrieved {len(liked_ids)} liked track IDs from user's Spotify library.")

    eng_tracks = spotify_service.search_tracks(genre + " english", limit=25)
    hin_tracks = spotify_service.search_tracks(genre + " hindi", limit=25)
    combined = eng_tracks + hin_tracks

    filtered = [t for t in combined if t["id"] not in liked_ids]
    logs.append(f"{len(filtered)} tracks remaining after filtering liked songs.")

    for t in filtered:
        t["explicit"] = bool(str(t.get("explicit", False)).lower() == "true")

    validated = validate_recommendations({"recommendations": filtered})
    if validated["validation_passed"]:
        final = validated["validated_output"]["recommendations"]
        logs.append(f"Guardrails passed: {len(final)} tracks are structurally valid.")
    else:
        logs.append("Guardrails failed. Returning empty recommendations.")
        return {"logs": logs, "recommendations": []}

    final_filtered = language_agent.filter_by_language(final, language)
    logs.append(f"{len(final_filtered)} tracks match the preferred language.")

    for i, track in enumerate(final_filtered, 1):
        logs.append(f"{i}. {track['name']} by {track['artist']} ({track.get('spotify_url')})")

    logs.append("✅ Recommendation flow completed successfully.")
    return {"logs": logs, "recommendations": final_filtered}
