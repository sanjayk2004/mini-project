import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API
SPOTIFY_CLIENT_ID = "3bab3dd2fd2343eea860292ecca7d41f"
SPOTIFY_CLIENT_SECRET = "671ad3eb396041d28f043f8d8f0c63ac"

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
        total_seeds = len(seed_artists or []) + len(seed_genres or [])
        if total_seeds < 5:
            st.write(f"⚠️ Adding default seeds to meet the requirement (you provided {total_seeds}).")

            # Add default genres if needed
            default_genres = ["pop", "rock", "classical", "jazz", "electronic"]
            seed_genres.extend(default_genres[:5 - total_seeds])

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
        # Split multiple genres into a list
        seed_genres = [g.strip().lower() for g in genre.split(",")]

    # Add language as a genre (Spotify doesn't support language directly)
    if language:
        # Map languages to valid Spotify genres
        language_to_genre = {
            "english": "pop",
            "hindi": "bollywood",
            "tamil": "tamil",
            "spanish": "latin",
            "korean": "k-pop"
        }
        for lang in language.split(","):
            lang = lang.strip().lower()
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
