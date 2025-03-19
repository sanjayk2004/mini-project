import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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
    if auth_response.status_code == 200:
        return auth_response.json()["access_token"]
    else:
        st.error("❌ Failed to get Spotify access token. Check your credentials.")
        return None

# Get Spotify access token
access_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

# Function to get Spotify recommendations
def get_spotify_recommendations(seed_artists=None, seed_genres=None, limit=10):
    """Get song recommendations from Spotify."""
    try:
        # Debug: Print seed values
        st.write(f"🔍 Seed Artists: {seed_artists}")
        st.write(f"🔍 Seed Genres: {seed_genres}")

        # Ensure at least 5 seeds are provided
        total_seeds = len(seed_artists or []) + len(seed_genres or [])
        if total_seeds < 5:
            st.write(f"⚠️ Adding default seeds to meet the requirement (you provided {total_seeds}).")

            # Add default genres if needed
            default_genres = ["pop", "rock", "classical", "jazz", "electronic"]
            seed_genres.extend(default_genres[:5 - total_seeds])

        # Ensure seed_artists and seed_genres are not None
        seed_artists = seed_artists or []
        seed_genres = seed_genres or []

        # Make the API request
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "seed_artists": ",".join(seed_artists),
            "seed_genres": ",".join(seed_genres),
            "limit": limit
        }
        response = requests.get(
            "https://api.spotify.com/v1/recommendations",
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            return response.json()["tracks"]
        else:
            st.error(f"❌ Spotify API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
        return None

# Streamlit UI
st.title("🎶 Music Recommendation System")

# Input Fields
st.write("### Enter your preferences:")
artist_name = st.text_input("Artist Name (optional)")
genre = st.text_input("Genre (optional, e.g., pop, rock, classical)")
language = st.text_input("Language (optional, e.g., english, hindi)")

# Get Recommendations Button
if st.button("Get Recommendations"):
    seed_artists = []
    seed_genres = []

    # Get artist ID if artist name is provided
    if artist_name and access_token:
        search_url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"q": f"artist:{artist_name}", "type": "artist", "limit": 1}
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            if results["artists"]["items"]:
                seed_artists = [results["artists"]["items"][0]["id"]]
            else:
                st.write(f"❌ No artist found with the name '{artist_name}'.")
        else:
            st.error(f"❌ Failed to search for artist: {response.status_code} - {response.text}")

    # Add genre if provided
    if genre:
        # Split multiple genres into a list and remove extra quotes
        seed_genres = [g.strip().lower().replace("'", "") for g in genre.split(",")]

    # Add language as a genre (Spotify doesn't support language directly)
    if language:
        # Map languages to valid Spotify genres
        language_to_genre = {
            "english": "pop",
            "hindi": "bollywood",
            "tamil": "world",
            "malayalam": "world",
            "spanish": "latin",
            "korean": "k-pop",
            "french": "french",
            "german": "german",
            "japanese": "j-pop",
            "chinese": "mandopop",
            "arabic": "arabic",
            "italian": "italian",
            "portuguese": "samba",
            "russian": "russian",
            "turkish": "turkish"
        }
        for lang in language.split(","):
            lang = lang.strip().lower().replace("'", "")
            if lang in language_to_genre:
                seed_genres.append(language_to_genre[lang])
            else:
                st.write(f"⚠️ Language '{lang}' is not supported. Using default genres instead.")

    # Ensure seed_genres is a list
    if not seed_genres:
        seed_genres = []

    # Get recommendations
    if seed_artists or seed_genres:
        recommendations = get_spotify_recommendations(seed_artists=seed_artists, seed_genres=seed_genres)
        if recommendations:
            st.write("🎧 Recommended Songs:")
            for track in recommendations:
                st.write(f"- **{track['name']}** by **{track['artists'][0]['name']}**")
                st.write(f"🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
    else:
        st.write("❌ Please provide at least an artist name or genre.")
