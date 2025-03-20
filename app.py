import streamlit as st
import requests
import time

# Spotify API credentials
SPOTIFY_CLIENT_ID = "3bab3dd2fd2343eea860292ecca7d41f"  # Replace with your actual Client ID
SPOTIFY_CLIENT_SECRET = "671ad3eb396041d28f043f8d8f0c63ac"  # Replace with your actual Client Secret

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    try:
        response = requests.post(
            auth_url,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret)
        )

        if response.status_code == 200:
            token_data = response.json()
            token_data["expires_at"] = time.time() + token_data["expires_in"]  # Add expiration time
            return token_data
        else:
            st.error(f"❌ Failed to get Spotify access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ An error occurred while fetching the access token: {e}")
        return None

# Function to check if the token is expired
def is_token_expired(token_data):
    if not token_data:
        return True  # Treat missing token as expired
    return time.time() >= token_data["expires_at"]

# Function to refresh the token if needed
def refresh_token_if_needed(token_data, client_id, client_secret):
    if is_token_expired(token_data):
        st.write("🔄 Refreshing access token...")
        return get_spotify_token(client_id, client_secret)
    return token_data

# Function to search for an artist
def search_artist(artist_name, access_token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"artist:{artist_name}", "type": "artist", "limit": 1}

    try:
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ Failed to search for artist: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ An error occurred while searching for the artist: {e}")
        return None

# Streamlit UI
st.title("🎶 Music Recommendation System")

# Input Fields
artist_name = st.text_input("Artist Name (optional)")

# Initialize token_data
token_data = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

# Get Recommendations Button
if st.button("Get Recommendations"):
    if not token_data:
        st.error("❌ Unable to retrieve Spotify access token. Please check your credentials.")
    else:
        # Refresh token if needed
        token_data = refresh_token_if_needed(token_data, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        access_token = token_data["access_token"] if token_data else None

        if not access_token:
            st.error("❌ Unable to retrieve Spotify access token. Please check your credentials.")
        else:
            # Search for the artist
            result = search_artist(artist_name, access_token)
            if result:
                st.write("✅ Artist Found:")
                st.json(result)  # Display the JSON response
            else:
                st.write("❌ Failed to fetch artist details.")
