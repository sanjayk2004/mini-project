import streamlit as st
import pandas as pd

# Function to load datasets from GitHub
@st.cache_data  # Cache data to avoid reloading on every interaction
def load_data():
    try:
        # URLs of the datasets hosted on GitHub
        dataset_urls = [
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/tcc_ceds_music.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Hindi_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Malayalam_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Tamil_songs.csv"
        ]

        # Load each dataset and combine them
        combined_data = pd.DataFrame()  # Empty DataFrame to hold combined data
        for i, url in enumerate(dataset_urls):
            try:
                st.write(f"Loading dataset {i + 1}...")
                data = pd.read_csv(url)
                st.write(f"Successfully loaded dataset {i + 1}.")
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            except Exception as e:
                st.error(f"Failed to load dataset {i + 1}: {url}")
                st.error(f"Error details: {e}")
                continue

        return combined_data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# Function to filter and recommend music
def recommend_music(release_date, artist, genre, data):
    if data is None:
        st.error("No data available to process recommendations.")
        return "No data available."

    # Start with the dataset
    filtered_data = data.copy()

    # Filter by release_date if the 'release_date' column exists
    if release_date:
        try:
            filtered_data = filtered_data[filtered_data['release_date'] == int(release_date)]
        except (KeyError, ValueError):
            st.warning("Invalid or missing 'release_date' column/inputs.")

    # Filter by artist if the 'artist_name' column exists
    if artist and 'artist_name' in filtered_data.columns:
        filtered_data['artist_name'] = filtered_data['artist_name'].astype(str)
        filtered_data = filtered_data[filtered_data['artist_name'].str.contains(artist, case=False, na=False)]

    # Filter by genre if the 'genre' column exists
    if genre and 'genre' in filtered_data.columns:
        filtered_data['genre'] = filtered_data['genre'].astype(str)
        filtered_data = filtered_data[filtered_data['genre'].str.contains(genre, case=False, na=False)]

    # Return top 100 recommendations or a message if no results found
    if filtered_data.empty:
        return "No recommendations found for the given inputs."

    # Return the filtered data with specified columns (only if they exist)
    available_columns = [col for col in ['track_name', 'artist_name', 'genre', 'release_date'] if col in filtered_data.columns]
    return filtered_data[available_columns].head(100)

# Streamlit App
def main():
    # Set page configuration
    st.set_page_config(
        page_title="🎵 Music Recommendation System",
        page_icon="🎵",
        layout="wide"
    )

    # Add a gradient-like background using HTML/CSS
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(to bottom, #6a11cb, #2575fc);
            color: white;
        }
        h1 {
            font-family: 'Poppins', sans-serif;
            text-align: center;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a stylish heading
    st.title("🎵 Music Recommendation System 🎵")

    # Initialize global variable for the dataset
    data = load_data()

    if data is None:
        st.error("Failed to load datasets. Please check the logs for more details.")
        return

    # Create input fields for release_date, artist, and genre
    st.subheader("Enter Your Preferences")
    release_date = st.text_input("Release Date:")
    artist = st.text_input("Artist Name:")
    genre = st.text_input("Genre:")

    # Button to get recommendations
    if st.button("Get Recommendations"):
        if not (release_date or artist or genre):
            st.warning("Please enter at least one filter (Release Date, Artist, or Genre).")
        else:
            recommendations = recommend_music(release_date, artist, genre, data)

            # Display the recommendations
            st.subheader("Recommendations")
            if isinstance(recommendations, pd.DataFrame):
                st.dataframe(recommendations)
            else:
                st.info(recommendations)

# Run the Streamlit app
if __name__ == "__main__":
    main()
    
