import streamlit as st
import requests

# Set up Spotify API
SPOTIFY_CLIENT_ID = "3bab3dd2fd2343eea860292ecca7d41f"
SPOTIFY_CLIENT_SECRET = "671ad3eb396041d28f043f8d8f0c63ac"

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    """Get an access token from Spotify."""
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        auth_url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret))
    
    # Debug: Print the response
    st.write(f"Auth Response Status Code: {auth_response.status_code}")
    st.write(f"Auth Response Text: {auth_response.text}")
    
    if auth_response.status_code == 200:
        return auth_response.json()["access_token"]
    else:
        st.error(f"❌ Failed to get Spotify access token. Status Code: {auth_response.status_code}")
        return None

# Get Spotify access token
access_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
if access_token:
    st.write("✅ Access Token:", access_token)
else:
    st.write("❌ Failed to retrieve access token.")
