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
        # Load CSV files with specified encoding to handle non-UTF-8 characters
        data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV, encoding="ISO-8859-1")
        data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV, encoding="ISO-8859-1")
        data_by_year = pd.read_csv(DATA_BY_YEAR_CSV, encoding="ISO-8859-1")
        data_w_genres = pd.read_csv(DATA_W_GENRES_CSV, encoding="ISO-8859-1")
        return data_by_artist, data_by_genres, data_by_year, data_w_genres
    except Exception as e:
        st.error(f"Failed to load CSV files: {e}")
        return None, None, None, None

# Streamlit Main App Function
def main():
    st.title("Music Recommendation System 🎵")
    st.write("This app provides song recommendations based on year, artist, and genre.")

    # Load the data
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # If any dataset is None or empty, show error and exit
    if any(df is None or df.empty for df in [data_by_artist, data_by_genres, data_by_year, data_w_genres]):
        st.error("Data could not be loaded or is empty. Please check your CSV files.")
        return

    # Debugging: Display the columns of data_by_artist to verify the structure
    st.write("### Debugging Information:")
    st.write("Columns in data_by_artist dataset:", data_by_artist.columns)

    # Check if 'artists' column exists and is valid
    if 'artists' in data_by_artist.columns:
        artist = st.selectbox("Select Artist", sorted(data_by_artist['artists'].dropna().unique()))
    else:
        st.error("The 'artists' column is missing in the data_by_artist dataset.")
        return

    # Check if 'year' column exists
    if 'year' in data_by_year.columns:
        year = st.selectbox("Select Year", sorted(data_by_year['year'].dropna().unique()))
    else:
        st.error("The 'year' column is missing in the data_by_year dataset.")
        return

    # Check if 'genres' column exists
    if 'genres' in data_by_genres.columns:
        genre = st.selectbox("Select Genre", sorted(data_by_genres['genres'].dropna().unique()))
    else:
        st.error("The 'genres' column is missing in the data_by_genres dataset.")
        return

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    st.write(recommendations)

# Music Recommendation Logic
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    try:
        # Filter the data based on year, artist, and genre
        filtered_data = data_by_year[data_by_year['year'] == int(year)]
        filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

        # Display top 10 recommendations (or all if fewer than 10)
        return filtered_data.head(10)
    except Exception as e:
        return f"Error during filtering: {e}"

if __name__ == "__main__":
    main()
