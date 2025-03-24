import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository
BASE_GITHUB_URL = "https://github.com/sanjayk2004/mini-project"
DATA_BY_ARTIST_CSV = https://github.com/sanjayk2004/mini-project+ "data_by_artist.csv"
DATA_BY_GENRES_CSV = https://github.com/sanjayk2004/mini-project + "data_by_genres (1).csv"
DATA_BY_YEAR_CSV = https://github.com/sanjayk2004/mini-project + "data_by_year (1).csv"
DATA_W_GENRES_CSV = https://github.com/sanjayk2004/mini-project + "data_w_genres.csv"

@st.cache_data
def load_data():
    # Load CSV files directly from GitHub URLs
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV)
    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV)
    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV)
    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV)
    return data_by_artist, data_by_genres, data_by_year, data_w_genres

# Streamlit Main App Function
def main():
    st.title("Music Recommendation System")

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
    # Filtering the data based on inputs
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist)]
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre)]
    
    # Display top recommendations
    return filtered_data.head(10)

if __name__ == "__main__":
    main()
