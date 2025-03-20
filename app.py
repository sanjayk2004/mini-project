import time
import requests

# Spotify API credentials
SPOTIFY_CLIENT_ID = "your_client_id"  # Replace with your actual Client ID
SPOTIFY_CLIENT_SECRET = "your_client_secret"  # Replace with your actual Client Secret

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
            print(f"❌ Failed to get Spotify access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ An error occurred while fetching the access token: {e}")
        return None

# Function to check if the token is expired
def is_token_expired(token_data):
    if not token_data:
        return True  # Treat missing token as expired
    return time.time() >= token_data["expires_at"]

# Function to refresh the token if needed
def refresh_token_if_needed(token_data, client_id, client_secret):
    if is_token_expired(token_data):
        print("🔄 Refreshing access token...")
        return get_spotify_token(client_id, client_secret)  # Regenerate token
    return token_data

# Function to search for an artist
def search_artist(artist_name, token_data):
    # Refresh token if needed
    token_data = refresh_token_if_needed(token_data, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    access_token = token_data["access_token"]

    search_url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"artist:{artist_name}", "type": "artist", "limit": 1}

    try:
        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            if results["artists"]["items"]:
                artist = results["artists"]["items"][0]
                print(f"✅ Found artist: {artist['name']} (ID: {artist['id']})")
                return artist
            else:
                print(f"❌ No artist found with the name '{artist_name}'.")
                return None
        else:
            print(f"❌ Failed to search for artist: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ An error occurred while searching for the artist: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Step 1: Generate the initial token
    token_data = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

    if not token_data:
        print("❌ Unable to retrieve Spotify access token. Please check your credentials.")
    else:
        # Step 2: Use the token to search for an artist
        artist_name = "Ed Sheeran"
        artist = search_artist(artist_name, token_data)

        if artist:
            print(f"Artist Details: {artist}")
        else:
            print("❌ Failed to fetch artist details.")
