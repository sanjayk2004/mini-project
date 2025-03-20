import streamlit as st
import requests
import time

# Set up Spotify API credentials
SPOTIFY_CLIENT_ID = "3bab3dd2fd2343eea860292ecca7d41f"
SPOTIFY_CLIENT_SECRET = "671ad3eb396041d28f043f8d8f0c63ac"

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"  # Correct authorization URL
    try:
        # Make the POST request to get the access token
        auth_response = requests.post(
            auth_url,
            data={"grant_type": "client_credentials"},  # Required parameter
            auth=(client_id, client_secret)  # Basic Authentication
        )

        # Check if the request was successful
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            token_data["expires_at"] = time.time() + token_data["expires_in"]  # Add expiration time
            return token_data
        else:
            st.error(f"❌ Failed to get Spotify access token: {auth_response.status_code} - {auth_response.text}")
            return None
    except Exception as e:
        st.error(f"❌ An error occurred while fetching the access token: {e}")
        return None

# Function to check if the token is expired
def is_token_expired(token_data):
    if not token_data:
        return True  # Treat missing token as expired
    return time.time() >= token_data["expires_at"]

# Function to refresh the token if expired
def refresh_token_if_needed(token_data, client_id, client_secret):
    if is_token_expired(token_data):
        st.write("🔄 Refreshing access token...")
        return get_spotify_token(client_id, client_secret)
    return token_data

# Function to get valid genres from Spotify
def get_valid_genres(access_token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        # Debugging: Print the access token
        st.write(f"🔑 Access Token: {access_token}")

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Debugging: Print the response
        st.write(f"🔍 Genre Seeds Response Status Code: {response.status_code}")
        st.write(f"🔍 Genre Seeds Response Body: {response.text}")

        if response.status_code == 200:
            return response.json()["genres"]
        else:
            st.error(f"❌ Failed to fetch valid genres: {response.status_code} - {response.text}")
            st.write("⚠️ Using default genres instead.")
            return [
                "pop", "rock", "classical", "jazz", "electronic",
                "hip-hop", "country", "blues", "reggae", "world"
            ]
    except Exception as e:
        st.error(f"❌ An error occurred while fetching valid genres: {e}")
        return []

# Function to get Spotify recommendations
def get_spotify_recommendations(access_token, seed_artists=None, seed_genres=None, limit=10):
    try:
        # Ensure at least 5 seeds are provided
        total_seeds = len(seed_artists or []) + len(seed_genres or [])
        if total_seeds < 5:
            default_genres = get_valid_genres(access_token)[:5 - total_seeds]
            seed_genres.extend(default_genres)

        # Ensure seed_artists and seed_genres are not None
        seed_artists = seed_artists or []
        seed_genres = seed_genres or []

        # Debugging: Print seeds
        st.write(f"🔍 Seed Artists: {seed_artists}")
        st.write(f"🔍 Seed Genres: {seed_genres}")

        # Make the API request
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "seed_artists": ",".join(seed_artists),
            "seed_genres": ",".join(seed_genres),
            "limit": limit
        }

        # Debugging: Print the final URL
        st.write(f"🔍 Final Recommendations URL: https://api.spotify.com/v1/recommendations?{requests.compat.urlencode(params)}")

        response = requests.get(
            "https://api.spotify.com/v1/recommendations",
            headers=headers,
            params=params
        )

        # Debugging: Print the response
        st.write(f"🎵 Response Status Code: {response.status_code}")
        st.write(f"🎵 Response Body: {response.text}")

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
artist_name = st.text_input("Artist Name (optional)")
genre = st.text_input("Genre (optional, e.g., pop, rock, classical)")
language = st.text_input("Language (optional, e.g., english, hindi)")

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
            seed_artists = []
            seed_genres = []

            # Get artist ID if artist name is provided
            if artist_name:
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
                seed_genres = [g.strip().lower().replace("'", "") for g in genre.split(",")]

            # Add language as a genre
            if language:
                language_to_genre = {
                    "english": "pop", "hindi": "bollywood", "tamil": "world", "malayalam": "world",
                    "spanish": "latin", "korean": "k-pop", "french": "french", "german": "german",
                    "japanese": "j-pop", "chinese": "mandopop", "arabic": "arabic", "italian": "italian",
                    "portuguese": "samba", "russian": "russian", "turkish": "turkish"
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
                recommendations = get_spotify_recommendations(access_token, seed_artists=seed_artists, seed_genres=seed_genres)
                if recommendations:
                    st.write("🎧 Recommended Songs:")
                    for track in recommendations:
                        st.write(f"- **{track['name']}** by **{track['artists'][0]['name']}**")
                        st.write(f"🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
            else:
                st.write("❌ Please provide at least an artist name or genre.")
