import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API
SPOTIFY_CLIENT_ID = "82db10b357f04e39bdced6d004526296"
SPOTIFY_CLIENT_SECRET = "b75e40d1ca0043f5ae836f393aa9f621"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Function to get Spotify recommendations
def get_spotify_recommendations(seed_artists=None, seed_genres=None, limit=10):
    """Get song recommendations from Spotify."""
    try:
        # Debug: Print seed values
        st.write(f"🔍 Seed Artists: {seed_artists}")
        st.write(f"🔍 Seed Genres: {seed_genres}")

        # Ensure at least 5 seeds are provided
        if (len(seed_artists or []) + len(seed_genres or [])) < 5:
            st.write("⚠️ Please provide at least 5 seeds (combined from artist and genre).")
            return None

        recommendations = sp.recommendations(
            seed_artists=seed_artists,
            seed_genres=seed_genres,
            limit=limit
        )
        return recommendations["tracks"]
    except spotipy.exceptions.SpotifyException as e:
        st.write(f"❌ Spotify API Error: {e}")
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
    if artist_name:
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if results["artists"]["items"]:
            seed_artists = [results["artists"]["items"][0]["id"]]
        else:
            st.write(f"❌ No artist found with the name '{artist_name}'.")

    # Add genre if provided
    if genre:
        seed_genres = [genre.strip().lower()]

    # Add language as a genre (Spotify doesn't support language directly)
    if language:
        seed_genres.append(language.strip().lower())

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
