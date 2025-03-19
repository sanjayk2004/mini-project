import streamlit as st
import soundfile as sf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Set up Spotify API
SPOTIFY_CLIENT_ID = "82db10b357f04e39bdced6d004526296"
SPOTIFY_CLIENT_SECRET = "b75e40d1ca0043f5ae836f393aa9f621"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Function to recognize a song using AudD API
def recognize_song(file_path):
    """Recognize a song using AudD API."""
    url = "https://api.audd.io/"
    data = {
        "api_token": "your_audd_api_token",  # Replace with your AudD API token
        "return": "spotify"
    }
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files).json()
    if response["status"] == "success":
        result = response["result"]
        if result:
            track_name = result["title"]
            artist = result["artist"]
            spotify_url = result["spotify"]["external_urls"]["spotify"]
            track_id = result["spotify"]["id"]
            return track_name, artist, spotify_url, track_id
    return None, None, None, None

# Function to get Spotify recommendations
def get_spotify_recommendations(seed_tracks, limit=5):
    """Get song recommendations from Spotify."""
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=limit)
    return recommendations["tracks"]

# Streamlit UI
st.title("🎶 Music Recognition & Recommendation System")

# Upload Audio File
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
if uploaded_file:
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.write("✅ File uploaded successfully!")
    st.audio(file_path, format="audio/wav")

    # Recognize the song
    track_name, artist, spotify_url, track_id = recognize_song(file_path)
    if track_name:
        st.write(f"🎵 Recognized: {track_name} by {artist}")
        st.write(f"🔗 [Listen on Spotify]({spotify_url})")

        # Get Spotify recommendations
        st.write("🎧 Recommended Songs:")
        recommendations = get_spotify_recommendations(seed_tracks=[track_id])
        for track in recommendations:
            st.write(f"- {track['name']} by {track['artists'][0]['name']}")
            st.write(f"🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
    else:
        st.write("❌ No match found.")

# Search a Song on Spotify
song_name = st.text_input("Enter a song name to search on Spotify")
if st.button("Search"):
    track_name, artist, spotify_url, track_id = search_song_on_spotify(song_name)
    if track_name:
        st.write(f"🎵 Found: {track_name} by {artist}")
        st.write(f"🔗 [Listen on Spotify]({spotify_url})")

        # Get Spotify recommendations
        st.write("🎧 Recommended Songs:")
        recommendations = get_spotify_recommendations(seed_tracks=[track_id])
        for track in recommendations:
            st.write(f"- {track['name']} by {track['artists'][0]['name']}")
            st.write(f"🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
    else:
        st.write("❌ No match found on Spotify.")
