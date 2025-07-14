from dotenv import load_dotenv
import os
from langgraph import Graph

from agents.Music_preferance_agent import MusicPreferenceAgent
from agents.language_filter import LanguageFilterAgent
from services.user_spotify_service import UserSpotifyService

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print(" Please set your OPENAI_API_KEY")
    exit(1)

preference_agent = MusicPreferenceAgent(openai_api_key)
language_agent = LanguageFilterAgent(openai_api_key)
spotify_service = UserSpotifyService()

def extract_preferences_node(user_input):
    preferences = preference_agent.extract_preferences(user_input)
    print(f" Extracted preferences: {preferences}")
    return {"preferences": preferences}

def recommend_tracks_node(state):
    preferences = state["preferences"]
    liked_ids = spotify_service.get_all_liked_song_ids()
    print(f"Retrieved {len(liked_ids)} liked songs")

    genre = preferences.get("genre", "pop")
    recommendations = spotify_service.search_tracks(genre, limit=20)
    filtered_recs = [
        track for track in recommendations if track.get("id") not in liked_ids
    ]

    print(f" Filtered down to {len(filtered_recs)} recommendations")

    return {**state, "recommendations": filtered_recs}


def language_filter_node(state):
    recs = state["recommendations"]
    user_prefs = state["preferences"]
    language = user_prefs.get("language", None)

    if language:
        filtered = language_agent.filter_by_language(recs, language)
        print(f" Language filtered down to {len(filtered)} tracks")
    else:
        filtered = recs
        print("No language specified, skipping filter")

    return {**state, "final_recommendations": filtered}

graph = Graph()

graph.add_node("extract_preferences", extract_preferences_node)
graph.add_node("recommend_tracks", recommend_tracks_node)
graph.add_node("language_filter", language_filter_node)

graph.add_edges([
    ("extract_preferences", "recommend_tracks"),
    ("recommend_tracks", "language_filter")
])

if __name__ == "__main__":
    user_input = input(" Enter your music preference: ")

    final_state = graph.run(user_input)
    final_recs = final_state.get("final_recommendations", [])

    if not final_recs:
        print(" No final recommendations to display.")
    else:
        print("\n Final recommended tracks:")
        for idx, track in enumerate(final_recs, 1):
            print(f"{idx}. {track['name']} by {track['artist']} (language={track.get('language', 'unknown')})")

    print("End of orchestration flow.")
