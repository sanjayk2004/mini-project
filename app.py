import streamlit as st
import soundfile as sf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment

# Set up Spotify API
SPOTIFY_CLIENT_ID = "82db10b357f04e39bdced6d004526296"
SPOTIFY_CLIENT_SECRET = "b75e40d1ca0043f5ae836f393aa9f621"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Function to load and play audio
def load_audio(file_path):
    """Load an audio file."""
    data, samplerate = sf.read(file_path)
    return data, samplerate

# Function to search for a song on Spotify
def search_song_on_spotify(song_name):
    """Search for a song on Spotify using the API."""
    results = sp.search(q=song_name, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        track_name = track["name"]
        artist = track["artists"][0]["name"]
        spotify_url = track["external_urls"]["spotify"]
        track_id = track["id"]
        return track_name, artist, spotify_url, track_id
    else:
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

# Play Audio Button
if st.button("Play Uploaded Audio"):
    if uploaded_file:
        audio_data, sr = load_audio(uploaded_file.name)
        st.audio(uploaded_file.name, format="audio/wav")
        st.write(f"📢 Playing at {sr} Hz")
    else:
        st.write("❌ No audio file uploaded.")

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
