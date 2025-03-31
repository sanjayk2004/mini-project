import streamlit as st
import pandas as pd
from time import sleep

# Function to load datasets from GitHub with a progress bar
@st.cache_data  # Cache data to avoid reloading on every interaction
def load_data():
    try:
        dataset_urls = [
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/tcc_ceds_music.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Hindi_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Malayalam_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Tamil_songs.csv"
        ]

        combined_data = pd.DataFrame()
        progress_text = st.empty()  # Placeholder for progress messages
        progress_bar = st.progress(0)  # Initialize progress bar

        for i, url in enumerate(dataset_urls):
            progress_text.text(f"Loading dataset {i + 1} of {len(dataset_urls)}...")
            progress_bar.progress((i + 1) / len(dataset_urls))  # Update progress
            try:
                data = pd.read_csv(url)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            except Exception as e:
                st.error(f"Failed to load dataset {i + 1}: {url}")
                st.error(f"Error details: {e}")
                continue

        progress_text.text("All datasets loaded successfully!")
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

    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        .stApp {
            background: #f9f9f9; /* Light gray background */
            color: #333333; /* Dark gray text */
        }
        h1 {
            font-family: 'Poppins', sans-serif;
            text-align: center;
            color: #333333; /* Dark gray heading */
        }
        .sidebar .sidebar-content {
            background: #ffffff; /* White sidebar background */
            color: #333333; /* Dark gray text */
        }
        .stButton>button {
            background-color: #ff9900; /* Orange button */
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }
        /* Change table header and row number colors */
        th {
            color: #333333 !important; /* Dark gray table headers */
        }
        td {
            color: #333333 !important; /* Dark gray table data */
        }
        /* Style for the GitHub link */
        a {
            color: #333333 !important; /* Dark gray link */
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a stylish heading
    st.title("🎵 Music Recommendation System 🎵")

    # Load data
    data = load_data()

    if data is None:
        st.error("Failed to load datasets. Please check the logs for more details.")
        return

    # Sidebar for inputs
    st.sidebar.subheader("🎵 Enter Your Preferences")
    with st.sidebar.form(key="recommendation_form"):
        release_date = st.text_input("Release Date:")
        artist = st.text_input("Artist Name:")
        genre = st.text_input("Genre:")

        # Submit button with "Enter" key support
        submit_button = st.form_submit_button(label="Get Recommendations")

    # Process recommendations when the form is submitted
    if submit_button:
        if not (release_date or artist or genre):
            st.warning("Please enter at least one filter (Release Date, Artist, or Genre).")
        else:
            recommendations = recommend_music(release_date, artist, genre, data)

            # Display the recommendations in the main area
            st.subheader("🎶 Recommendations")
            if isinstance(recommendations, pd.DataFrame):
                st.table(recommendations.style.set_properties(**{
                    'background-color': '#ffffff', /* White table background */
                    'color': '#333333', /* Dark gray table text */
                    'border-color': '#cccccc'
                }))
            else:
                st.info(recommendations)

    # Add an expander for instructions
    with st.expander("ℹ️ How to Use This App"):
        st.write("""
        1. Enter your preferences in the sidebar (e.g., Release Date, Artist, Genre).
        2. Press "Get Recommendations" or hit the "Enter" key.
        3. View up to 100 song recommendations based on your inputs.
        """)

    # Add an expander for dataset details
    with st.expander("📊 Dataset Details"):
        st.write("""
        This app combines data from multiple datasets:
        - tcc_ceds_music.csv
        - Hindi_songs.csv
        - Malayalam_songs.csv
        - Tamil_songs.csv
        """)

# Run the Streamlit app
if __name__ == "__main__":
    main()
