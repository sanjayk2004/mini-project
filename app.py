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

    # Example: Search for an artist
    artist_name = "Ed Sheeran"
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}

    search_response = requests.get(search_url, headers=headers, params=params)
    
    # Debug: Print the search response
    st.write(f"Search Response Status Code: {search_response.status_code}")
    st.write(f"Search Response Text: {search_response.text}")

    if search_response.status_code == 200:
        results = search_response.json()
        if results["artists"]["items"]:
            artist = results["artists"]["items"][0]
            st.write(f"🎵 Found Artist: {artist['name']}")
            st.write(f"🔗 Spotify URL: {artist['external_urls']['spotify']}")
        else:
            st.write(f"❌ No artist found with the name '{artist_name}'.")
    else:
        st.error(f"❌ Failed to search for artist. Status Code: {search_response.status_code}")
else:
    st.write("❌ Failed to retrieve access token.")
