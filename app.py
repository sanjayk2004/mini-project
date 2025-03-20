import streamlit as st
import requests

# Your valid access token
access_token = "BQAtdNqKlvAofq-nD_3LYVhCiQ1LUX9qNUeJgujV5v8gqbSuxV0LONHmJW5FCFg_BdpgsvK0wAQqFLbwicwlHS5caUayfjMd2ZXG_sZ8CIr9x2XCvK3zPZnIpLKGMk7acETMaIsoouE"

# Function to search for an artist and return their ID
def get_artist_id(artist_name, access_token):
    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"artist:{artist_name}", "type": "artist", "limit": 1}

    try:
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            if results["artists"]["items"]:
                artist_id = results["artists"]["items"][0]["id"]
                st.write(f"✅ Found artist: {results['artists']['items'][0]['name']} (ID: {artist_id})")
                return artist_id
            else:
                st.error(f"❌ No artist found with the name '{artist_name}'.")
                return None
        else:
            st.error(f"❌ Failed to search for artist: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ An error occurred while searching for the artist: {e}")
        return None

# Function to get song recommendations
def get_recommendations(seed_artists=None, seed_genres=None, limit=10):
    recommendations_url = "https://api.spotify.com/v1/recommendations"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "seed_artists": ",".join(seed_artists or []),
        "seed_genres": ",".join(seed_genres or []),
        "limit": limit
    }

    try:
        response = requests.get(recommendations_url, headers=headers, params=params)

        if response.status_code == 200:
            recommendations = response.json()["tracks"]
            st.write("🎧 Recommended Songs:")
            for track in recommendations:
                st.write(f"- **{track['name']}** by **{track['artists'][0]['name']}**")
                st.write(f"  🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
        else:
            st.error(f"❌ Failed to fetch recommendations: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"❌ An error occurred while fetching recommendations: {e}")

# Streamlit UI
st.title("🎶 Music Recommendation System")

# Input Fields
artist_name = st.text_input("Artist Name (optional)")
genre = st.text_input("Genre (optional, e.g., pop, rock, classical)")

# Get Recommendations Button
if st.button("Get Recommendations"):
    if not artist_name and not genre:
        st.error("❌ Please provide at least an artist name or genre.")
    else:
        seed_artists = []
        seed_genres = []

        # Get artist ID if artist name is provided
        if artist_name:
            artist_id = get_artist_id(artist_name, access_token)
            if artist_id:
                seed_artists.append(artist_id)

        # Add genre if provided
        if genre:
            seed_genres = [g.strip().lower() for g in genre.split(",")]

        # Get recommendations
        if seed_artists or seed_genres:
            get_recommendations(seed_artists=seed_artists, seed_genres=seed_genres)
        else:
            st.error("❌ Please provide valid seeds (artist or genre).")
