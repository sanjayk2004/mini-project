import streamlit as st
import requests
import os
import pyaudio
import wave
import threading
import http.client
import json
import numpy as np

# Deezer API Key (replace with your actual API key)
DEEZER_API_KEY = "ed97f96fa6msh2f690d775cfbf43p1263f5jsnd1ecb8905406"
DEEZER_API_HOST = "deezerdevs-deezer.p.rapidapi.com"

# Shazam API Key (via RapidAPI)
SHAZAM_API_KEY = "e3c7c2cd8amshc47ae7d373ca8d1p1a78c9jsna8f3a8d2ec7f"
SHAZAM_API_HOST = "shazam-api6.p.rapidapi.com"

# Audio recording settings
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILENAME = "recorded_audio.wav"

# History to store last 10 recognized songs
history = []

def recognize_music_with_shazam(file_path):
    """Send the audio file to Shazam API for music recognition."""
    url = f"https://{SHAZAM_API_HOST}/songs/detect"
    headers = {
        "X-RapidAPI-Key": SHAZAM_API_KEY,
        "X-RapidAPI-Host": SHAZAM_API_HOST,
        "Content-Type": "application/json"
    }
    
    try:
        with open(file_path, "rb") as file:
            audio_data = file.read()
        response = requests.post(url, headers=headers, data=audio_data)
        response.raise_for_status()  # Raise an error for bad responses
        response_json = response.json()
        
        if "track" in response_json:
            return response_json["track"]
        else:
            st.error("Recognition failed: " + str(response_json))
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def fetch_deezer_artist_info(artist_name):
    """Fetch artist information from Deezer API."""
    conn = http.client.HTTPSConnection(DEEZER_API_HOST)
    headers = {
        'x-rapidapi-key': DEEZER_API_KEY,
        'x-rapidapi-host': DEEZER_API_HOST
    }
    
    conn.request("GET", f"/search?q={artist_name}", headers=headers)
    res = conn.getresponse()
    
    if res.status == 200:
        data = res.read()
        response_json = json.loads(data.decode("utf-8"))
        if response_json.get("data"):
            return response_json["data"][0]
        else:
            return None
    return None

def update_history(song, artist):
    """Update the history list with the latest recognized song."""
    if len(history) >= 10:
        history.pop(0)
    history.append(f"{song} by {artist}")

def display_results(results):
    """Display music recognition results and recommendations."""
    if results:
        song = results.get("title", "Unknown")
        artist = results.get("subtitle", "Unknown")
        album = results.get("sections", [{}])[0].get("metadata", [{}])[0].get("text", "Unknown")
        
        result_text = f"**Song:** {song}\n**Artist:** {artist}\n**Album:** {album}"
        
        artist_info = fetch_deezer_artist_info(artist)
        if artist_info:
            deezer_info = f"\n\n**Deezer Info:**\n**Artist:** {artist_info.get('name', 'N/A')}\n**Followers:** {artist_info.get('fans', 'N/A')}"
            result_text += deezer_info
        
        update_history(song, artist)
        st.success(result_text)
    else:
        st.error("Error: Music could not be recognized. Please try again.")

def record_audio():
    """Record audio and save it to a file."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    
    st.write("Recording...")
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(OUTPUT_FILENAME, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
    
    st.success(f"Recording saved as {OUTPUT_FILENAME}")
    results = recognize_music_with_shazam(OUTPUT_FILENAME)
    display_results(results)

# Streamlit Layout
st.title("Music Recognition System")
st.write("Upload an audio file or record your own to recognize music.")

# Upload audio file
uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])
if uploaded_file is not None:
    with open(OUTPUT_FILENAME, "wb") as f:
        f.write(uploaded_file.getbuffer())
    results = recognize_music_with_shazam(OUTPUT_FILENAME)
    display_results(results)

# Record audio button
if st.button("Record Audio"):
    record_audio()

# Show history
if st.button("Show History"):
    if history:
        st.write("Recognition History:")
        for entry in history:
            st.write(entry)
    else:
        st.write("No history available.")

# Quit button (not necessary in Streamlit, but can be used to stop the app)
if st.button("Quit"):
    st.stop()
