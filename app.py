import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import soundfile as sf
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API
SPOTIFY_CLIENT_ID = "82db10b357f04e39bdced6d004526296"
SPOTIFY_CLIENT_SECRET = "b75e40d1ca0043f5ae836f393aa9f621"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                           client_secret=SPOTIFY_CLIENT_SECRET))

# Function to record audio
def record_audio():
    """Record audio and save it to a file."""
    duration = 5  # Record for 5 seconds
    sample_rate = 44100  # Sampling rate
    st.write("🎤 Recording... Speak now!")

    # Record the audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()  # Wait for recording to finish

    # Save as WAV file
    filename = "./recorded_audio.wav"
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

    st.write("✅ Recording finished! Saved as", filename)
    return filename

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
        return f"🎵 Found: {track_name} by {artist}\n🔗 [Listen on Spotify]({spotify_url})"
    else:
        return "❌ No match found on Spotify."

# Streamlit UI
st.title("🎶 Music Recognition & Recommendation System")

# Record Audio Button
if st.button("Record Audio"):
    recorded_file = record_audio()
    if recorded_file:
        st.audio(recorded_file, format="audio/wav")

# Upload Audio File
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
if uploaded_file:
    file_path = f"./{uploaded_file.name}"  # Use the actual name of the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.write("✅ File uploaded successfully!")
    st.audio(file_path, format="audio/wav")

# Play Audio Button
if st.button("Play Recorded Audio"):
    file_to_play = "recorded_audio.wav" if not uploaded_file else uploaded_file.name
    audio_data, sr = load_audio(file_to_play)
    st.audio(file_to_play, format="audio/wav")
    st.write(f"📢 Playing at {sr} Hz")

# Search a Song on Spotify
song_name = st.text_input("Enter a song name to search on Spotify")
if st.button("Search"):
    result = search_song_on_spotify(song_name)
    st.markdown(result)
