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
        # Load CSV files directly from GitHub URLs with specified encoding
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

    if data_by_year is not None:
        # Display basic info if CSVs load correctly
        st.write("## Sample Table from Data by Year:")
        st.write(data_by_year.head())

        # Inputs from the user
        year = st.selectbox("Select Year", sorted(data_by_year['year'].unique()))
        artist = st.selectbox("Select Artist", sorted(data_by_artist['artists'].unique()))
        genre = st.selectbox("Select Genre", sorted(data_by_genres['genres'].unique()))

        st.write("### Recommended Songs Based on Your Inputs:")
        recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
        st.write(recommendations)
    else:
        st.error("Data could not be loaded. Please check your file paths and try again.")

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
