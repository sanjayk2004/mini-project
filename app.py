import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository (direct downloadable links)
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"  # Use the 'raw' link
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres%20(1).csv"  # Handle special characters like space with %20
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year%20(1).csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    # Load CSV files directly from the GitHub URLs
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV)
    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV)
    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV)
    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV)
    return data_by_artist, data_by_genres, data_by_year, data_w_genres

# Streamlit Main App Function
def main():
    st.title("Music Recommendation System")

    # Load the data
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Inputs from the user
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    st.write(recommendations)

# Music Recommendation Logic
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    # Filter the data based on inputs
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

    # Display top recommendations
    return filtered_data.head(10)

if __name__ == "__main__":
    main()
