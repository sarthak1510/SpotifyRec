🎧 Personalised Music Recommendation Agentic System

🧠 Multi-Agent LLM System for Personalized Music RecommendationsFastAPI + OpenAI API's + Spotify OAuth + Streamlit


📌 Summary
This is a multi-agent orchestration system that converts free-form natural language prompts (e.g. "hindi sad r&b for gym") into personalized Spotify recommendations. Built with a modular AI architecture that leverages LLM agents, guardrails, and user-authenticated data flows, this project simulates real-world production AI deployment.

🧠 Key Features & Architecture Highlights



Layer
Description



🧠 LLM-Oriented Agents
Modular agents (LLMs) handle preference extraction, language detection, and filtering


🔁 Multi-Agent Pipeline
Orchestrated flow between GPT-based agents and Spotify services


🔒 User-Centric OAuth
Spotify OAuth 2.0 with dynamic token refresh and safe session persistence


✅ Guardrails Validation
Output validation with validate_recommendations() ensures safety and quality


🧠 Language Filter Agent
NLP-based filtering of track results based on user’s linguistic preference


🎧 Spotify Service Layer
Authenticated search, liked song history exclusion, metadata handling


🖥️ Streamlit Frontend
Lightweight UI to interface with the system and trigger recommendation flows


⚙️ Production API
RESTful FastAPI backend with scalable deployment on Render



🧱 Modular Tech Stack



Component
Tech Stack



AI Agents
OpenAI GPT, custom multi-agent system


Backend API
FastAPI, Uvicorn, Render


Auth Layer
Spotify OAuth 2.0, Spotipy


Frontend
Streamlit


Env Management
.env, Render Environment Variables


Validation
Custom guardrails.py module



🏗️ Multi-Agent System Architecture
[User Prompt]
     ↓
[Streamlit UI]
     ↓
[FastAPI /@recommend]
     ↓
┌──────────────────────────────┐
│  MusicPreferenceAgent (LLM) │  ← GPT-based genre/mood extractor
└────────────┬────────────────┘
             ↓
┌──────────────────────────────┐
│     SpotifyService Layer     │  ← Spotify search, liked songs filtering
└────────────┬────────────────┘
             ↓
┌──────────────────────────────┐
│   Guardrails + Deduplication │  ← Validates, removes explicit, ensures structure
└────────────┬────────────────┘
             ↓
┌──────────────────────────────┐
│   LanguageFilterAgent (LLM)  │  ← Filters results by detected language
└────────────┬────────────────┘
             ↓
      Final Recommendation JSON

📦 Project Structure
.
├── api_server.py                # FastAPI application entrypoint
├── main.py                      # CLI prompt test interface (dev only)
├── services/
│   ├── spotify_service.py       # Spotify API logic (tracks, search, metadata)
│   └── user_spotify_service.py  # OAuth handling, liked songs, token refresh
├── agents/
│   ├── Music_preferance_agent.py # GPT-based preference extractor agent
│   └── language_filter.py        # LanguageFilterAgent using LLM
├── utils/
│   └── guardrails.py            # Output validation, filtering
├── frontend/
│   └── streamlit_app.py         # Minimalist frontend for testing agents
├── .env                         # Local development env variables
└── README.md                    # Project documentation

🔐 Environment Variables (Render Deployment)
Create a .env file with the following variables:
OPENAI_API_KEY=Your OpenAI GPT API key
SPOTIPY_CLIENT_ID=Spotify Developer Client ID
SPOTIPY_CLIENT_SECRET=Spotify Developer Client Secret
SPOTIFY_ACCESS_TOKEN=Pre-generated user access token
SPOTIFY_REFRESH_TOKEN=Long-lived Spotify refresh token
SPOTIFY_EXPIRES_AT=Expiry timestamp in epoch format
SPOTIPY_REDIRECT_URI=Redirect URI for Spotify auth callback

⚙️ Local Setup & Usage
🔧 Backend (FastAPI)

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Start the FastAPI server:
uvicorn api_server:app --reload --port 8000


Test the backend using Postman:
POST http://localhost:8000/recommend
Body: { "prompt": "hindi sad r&b for gym" }



🖥️ Frontend (Streamlit)

Run the Streamlit UI:
streamlit run frontend/streamlit_app.py


Update the API URL in frontend/streamlit_app.py:
API_URL = "https://your-backend.onrender.com/recommend"



🧪 Sample Prompts

"Punjabi dance hits for parties"
"english indie heartbreak"
"hindi motivational gym vibes"
"bollywood romantic acoustic classics"

📤 Sample Output (JSON)
{
  "recommendations": [
    {
      "name": "Tum Hi Ho",
      "artist": "Arijit Singh",
      "spotify_url": "https://open.spotify.com/track/xyz",
      "explicit": false
    },
    {
      "name": "Kesariya",
      "artist": "Arijit Singh",
      "spotify_url": "https://open.spotify.com/track/abc",
      "explicit": false
    }
  ]
}

