import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository (direct downloadable links)
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres%20(1).csv"
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year%20(1).csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    # Load and clean CSV data (ensure consistent column formatting)
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV, encoding='ISO-8859-1')
    data_by_artist.columns = data_by_artist.columns.str.strip().str.lower()  # Trim spaces, lowercase
    
    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV, encoding='ISO-8859-1')
    data_by_genres.columns = data_by_genres.columns.str.strip().str.lower()
    
    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV, encoding='ISO-8859-1')
    data_by_year.columns = data_by_year.columns.str.strip().str.lower()
    
    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV, encoding='ISO-8859-1')
    data_w_genres.columns = data_w_genres.columns.str.strip().str.lower()
    
    return data_by_artist, data_by_genres, data_by_year, data_w_genres

def main():
    st.title("Music Recommendation System")

    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Print columns for debugging (optional)
    st.write("Available columns in 'data_by_artist':", data_by_artist.columns.tolist())

    # Inputs from the user
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    st.write(recommendations)

def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    # Filter and recommend songs (using unified lowercase, no spaces)
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

    return filtered_data.head(10)

if __name__ == "__main__":
    main()
