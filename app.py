import streamlit as st
import requests
import os
import base64
import json
import wave
import pydub
from pydub import AudioSegment
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = '82db10b357f04e39bdced6d004526296'
CLIENT_SECRET = 'b75e40d1ca0043f5ae836f393aa9f621'

# Function to get access token from Spotify
def get_spotify_token():
    client_credentials = f"{82db10b357f04e39bdced6d004526296}:{b75e40d1ca0043f5ae836f393aa9f621}"
    client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {client_credentials_b64}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        st.error("Unable to get access token")
        return None

# Function to search for song using Spotify API
def search_song(song_name, access_token):
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        track = data["tracks"]["items"][0]
        return {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "url": track["external_urls"]["spotify"]
        }
    else:
        return None

# Function to get recommendations from Spotify API
def get_recommendations(track_id, access_token):
    url = f"https://api.spotify.com/v1/recommendations?seed_tracks={track_id}&limit=5"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        recommendations = [
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "url": track["external_urls"]["spotify"]
            }
            for track in data["tracks"]
        ]
        return recommendations
    else:
        return None

# Function to handle the audio recording and recognition
def record_audio():
    """Record audio and save it to a file."""
    audio = pydub.AudioSegment.from_file("path_to_audio_file.wav")  # Replace with actual recording code
    
    st.write("Recording finished!")
    audio.export("recorded_audio.wav", format="wav")
    st.success("Audio saved as recorded_audio.wav")
    access_token = get_spotify_token()
    if access_token:
        track_info = search_song("Shape of You", access_token)  # Replace with song recognition logic
        if track_info:
            st.write(track_info)
            recommendations = get_recommendations(track_info['url'], access_token)
            if recommendations:
                st.write("Recommendations:")
                for rec in recommendations:
                    st.write(f"{rec['name']} by {rec['artist']}")
            else:
                st.write("No recommendations found.")
        else:
            st.write("Song not found.")

# Streamlit Layout
st.title("Music Recognition and Recommendation System")
st.write("Upload an audio file or record your own to recognize music and get recommendations.")

# Upload audio file
uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "m4a"])
if uploaded_file is not None:
    with open("uploaded_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    access_token = get_spotify_token()
    if access_token:
        track_info = search_song("Shape of You", access_token)  # Replace with actual song recognition logic
        if track_info:
            st.write(track_info)
            recommendations = get_recommendations(track_info['url'], access_token)
            if recommendations:
                st.write("Recommendations:")
                for rec in recommendations:
                    st.write(f"{rec['name']} by {rec['artist']}")
            else:
                st.write("No recommendations found.")
        else:
            st.write("Song not found.")

# Record audio button
if st.button("Record Audio"):
    record_audio()

# Show history button
if st.button("Show History"):
    st.write("Recognition History:")  # Add functionality to display recognition history if needed

# Quit button (not necessary in Streamlit, but can be used to stop the app)
if st.button("Quit"):
    st.stop()
