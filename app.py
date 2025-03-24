import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres.csv"
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year.csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    try:
        # Load CSV data with appropriate encoding and verify columns
        data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV, encoding="ISO-8859-1")
        data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV, encoding="ISO-8859-1")
        data_by_year = pd.read_csv(DATA_BY_YEAR_CSV, encoding="ISO-8859-1")
        data_w_genres = pd.read_csv(DATA_W_GENRES_CSV, encoding="ISO-8859-1")
        return data_by_artist, data_by_genres, data_by_year, data_w_genres
    except Exception as e:
        st.error(f"Failed to load CSV files: {e}")
        return None, None, None, None

def main():
    st.title("Music Recommendation System 🎵")
    st.write("This app provides song recommendations based on year, artist, and genre.")

    # Load the data
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Verify if datasets loaded correctly
    if any(df is None or df.empty for df in [data_by_artist, data_by_genres, data_by_year, data_w_genres]):
        st.error("Data could not be loaded or is empty. Please check your CSV files.")
        return

    # Show available columns for debugging (optional)
    st.write("### Columns in Each Dataset:")
    st.write("data_by_artist:", data_by_artist.columns.tolist())
    st.write("data_by_genres:", data_by_genres.columns.tolist())
    st.write("data_by_year:", data_by_year.columns.tolist())
    st.write("data_w_genres:", data_w_genres.columns.tolist())

    # Artist selection
    artist = st.selectbox("Select Artist", sorted(data_by_artist['artists'].dropna().unique())) if 'artists' in data_by_artist.columns else None

    # Year selection from data_by_year
    year = st.selectbox("Select Year", sorted(data_by_year['year'].dropna().unique())) if 'year' in data_by_year.columns else None

    # Genre selection from the dedicated genres dataset
    genre = st.selectbox("Select Genre", sorted(data_by_genres['genres'].dropna().unique())) if 'genres' in data_by_genres.columns else None

    if not (artist and year and genre):
        st.error("Please ensure 'artist', 'year', and 'genre' are correctly selected.")
        return

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, genre, data_by_year, data_w_genres)
    st.write(recommendations)

def recommend_music(year, genre, data_by_year, data_w_genres):
    try:
        # Validate columns before merging
        if 'year' not in data_by_year.columns:
            return "Error: 'year' column is missing from data_by_year dataset."
        if 'genres' not in data_w_genres.columns:
            return "Error: 'genres' column is missing from data_w_genres dataset."

        # Filter by year
        filtered_data = data_by_year[data_by_year['year'] == int(year)]

        st.write("Columns in filtered_data after filtering by year:", filtered_data.columns)

        # Filter by genre using `data_w_genres` (since it contains additional genre-related song info)
        filtered_data = pd.merge(filtered_data, data_w_genres, on='year', how='inner')
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

        if filtered_data.empty:
            return "No matching songs found based on your filters."

        # Display top 10 songs from the filtered dataset
        return filtered_data.head(10)
    except Exception as e:
        return f"Error during filtering: {e}"

if __name__ == "__main__":
    main()
