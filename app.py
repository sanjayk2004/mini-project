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
                print(f"✅ Found artist: {results['artists']['items'][0]['name']} (ID: {artist_id})")
                return artist_id
            else:
                print(f"❌ No artist found with the name '{artist_name}'.")
                return None
        else:
            print(f"❌ Failed to search for artist: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ An error occurred while searching for the artist: {e}")
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
            print("🎧 Recommended Songs:")
            for track in recommendations:
                print(f"- **{track['name']}** by **{track['artists'][0]['name']}**")
                print(f"  🔗 [Listen on Spotify]({track['external_urls']['spotify']})")
        else:
            print(f"❌ Failed to fetch recommendations: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ An error occurred while fetching recommendations: {e}")

# Main logic
if __name__ == "__main__":
    # Step 1: Search for an artist
    artist_name = "Ed Sheeran"
    artist_id = get_artist_id(artist_name, access_token)

    if artist_id:
        # Step 2: Get song recommendations
        seed_artists = [artist_id]  # Use the artist ID as a seed
        seed_genres = ["pop", "soft pop"]  # Add relevant genres
        get_recommendations(seed_artists=seed_artists, seed_genres=seed_genres)
