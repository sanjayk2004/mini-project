import streamlit as st
import requests
import os
import wave
import numpy as np
import base64

# Deezer API Key (replace with your actual API key)
DEEZER_API_KEY = "ed97f96fa6msh2f690d775cfbf43p1263f5jsnd1ecb8905406"
DEEZER_API_HOST = "deezerdevs-deezer.p.rapidapi.com"

# Shazam API Key (via RapidAPI)
SHAZAM_API_KEY = "e3c7c2cd8amshc47ae7d373ca8d1p1a78c9jsna8f3a8d2ec7f"
SHAZAM_API_HOST = "shazam-api6.p.rapidapi.com"

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

def save_audio(base64_audio_data, file_path="recorded_audio.wav"):
    """Save base64 audio data to a file."""
    audio_data = base64.b64decode(base64_audio_data)
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_data)
    return file_path

# Streamlit Layout
st.title("Music Recognition System")
st.write("Record your song using the button below.")

# HTML and JavaScript code to record audio
audio_html = """
    <html>
    <body>
    <h2>Record Your Song</h2>
    <script>
    var recorder, audio_stream, audio_data = [];
    function startRecording() {
        navigator.mediaDevices.getUserMedia({audio: true}).then(function(stream) {
            audio_stream = stream;
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = function(e) { audio_data.push(e.data); };
            recorder.onstop = function() {
                var blob = new Blob(audio_data, { type: 'audio/wav' });
                var reader = new FileReader();
                reader.onloadend = function() {
                    var base64Audio = reader.result.split(',')[1];
                    window.parent.postMessage(base64Audio, "*");
                };
                reader.readAsDataURL(blob);
            };
            recorder.start();
            document.getElementById('status').innerHTML = "Recording...";
        });
    }

    function stopRecording() {
        recorder.stop();
        audio_stream.getTracks().forEach(track => track.stop());
        document.getElementById('status').innerHTML = "Recording stopped.";
    }
    </script>
    <button onclick="startRecording()">Start Recording</button>
    <button onclick="stopRecording()">Stop Recording</button>
    <p id="status">Recording status will be displayed here.</p>
    </body>
    </html>
"""

# Use st.components.v1 to embed the HTML and JavaScript for recording
from streamlit.components.v1 import html

# Embed the audio recording HTML/JS
html(audio_html, height=400)

# Listen for the base64 audio data from the frontend (JavaScript)
audio_data = st.experimental_get_query_params().get("audio", None)
if audio_data:
    file_path = save_audio(audio_data[0])
    results = recognize_music_with_shazam(file_path)
    display_results(results)

# Show history
if st.button("Show History"):
    if history:
        st.write("Recognition History:")
        for entry in history:
            st.write(entry)
    else:
        st.write("No history available.")
