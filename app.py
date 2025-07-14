import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/recommend")

spotify_svg = """
<svg xmlns="http://www.w3.org/2000/svg" height="32" viewBox="0 0 168 168" width="32"><path fill="#1ED760" d="M84,0C37.7,0,0,37.7,0,84s37.7,84,84,84s84-37.7,84-84S130.3,0,84,0z M122.5,120.9c-1.5,2.5-4.7,3.3-7.2,1.8
c-19.8-12.1-44.8-14.9-74.2-8.4c-2.9,0.6-5.8-1.3-6.4-4.3c-0.6-2.9,1.3-5.8,4.3-6.4c32.5-7,60.3-3.7,83.4,10
C123.2,115.2,124,118.4,122.5,120.9z M135.4,96.2c-1.9,3-5.8,3.9-8.8,2c-22.7-14-57.3-18.1-84.2-10.2c-3.4,1-7-0.9-8-4.3
c-1-3.4,0.9-7,4.3-8c31.8-9.3,70.2-4.6,96.7,12.2C136.4,89.3,137.3,93.2,135.4,96.2z M137.4,71.1c-27.3-16.6-72.3-18.1-98-10.1
c-4,1.3-8.2-1-9.5-5c-1.3-4,1-8.2,5-9.5c30.7-9.6,81.5-7.9,113.1,11.5c3.6,2.2,4.8,6.9,2.6,10.5C147.9,72.1,143,73.3,137.4,71.1z"/></svg>
"""

st.set_page_config(page_title="Personalized Music Recommendation Agent", layout="centered")
spotify_dark = "#191414"
spotify_green = "#1DB954"

st.markdown(f"""
    <style>
        html, body, .stApp {{
            background-color: {spotify_dark};
            color: white !important;
        }}
        a {{
            color: {spotify_green} !important;
        }}
        h1 {{
            color: {spotify_green};
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 1rem;
        }}
        .log-box {{
            font-family: monospace;
            background: none;
            padding: 10px;
            white-space: pre-wrap;
            font-size: 14px;
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<h1>{spotify_svg} Personalized Music Recommendation Agent</h1>", unsafe_allow_html=True)

st.markdown("Enter your music preference based on language, genre, mood or explicit/non-explicit:")
user_input = st.text_input("", placeholder="e.g. hindi happy metal")

if user_input:
    log_text = ""

    with st.spinner("Getting recommendations..."):
        try:
            res = requests.post(API_URL, json={"prompt": user_input}, timeout=300)
            data = res.json()
            logs = data.get("logs", [])
            recommendations = data.get("recommendations", [])

            for log in logs:
                log_text += log + "\n"
                if "Retrieved" in log and "liked track IDs" in log:
                    break  # Stop logs here

            st.markdown(f"<div class='log-box'>{log_text.strip()}</div>", unsafe_allow_html=True)

            if recommendations:
                st.markdown(f"<h3 style='color:{spotify_green};'>🎧 Final Recommendations</h3>", unsafe_allow_html=True)
                for i, track in enumerate(recommendations, 1):
                    name = track.get("name", "Unknown")
                    artist = track.get("artist", "Unknown")
                    url = track.get("spotify_url", "#")
                    st.markdown(f"**{i}.** [{name} by {artist}]({url})", unsafe_allow_html=True)
                st.success("Recommendation flow completed successfully.")
            else:
                st.warning("No tracks matched your preferences.")

        except requests.exceptions.Timeout:
            st.error("❌ Request timed out.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
