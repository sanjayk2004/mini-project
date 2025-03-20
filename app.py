import streamlit as st
import requests

# Spotify API access token
access_token = "BQCVSDkFUDB3PenbS9PUAh8K9ZNKc88JZiLajVWRQoZXFTTVJ3XBwKgQYdSbeHeiq4wCqVEnPMRTtIwjnrWUiwwhkIp_zrzx2z78gMvuLH2Fcg8m2yLVRlxfyabXasGDbP9VJpduKRs"

# Search for an artist
def search_artist(artist_name, access_token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"artist:{artist_name}", "type": "artist", "limit": 1}

    try:
        # Debugging: Print the headers
        st.write(f"🔍 Headers: {headers}")

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

# Get Recommendations Button
if st.button("Get Recommendations"):
    if not access_token:
        st.error("❌ No access token provided.")
    else:
        # Search for the artist
        result = search_artist(artist_name, access_token)
        if result:
            st.write("✅ Artist Found:")
            st.json(result)  # Display the JSON response
        else:
            st.write("❌ Failed to fetch artist details.")
