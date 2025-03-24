import pandas as pd
import streamlit as st
from urllib.parse import quote  # For URL encoding

# URLs of the CSV files in your GitHub repository (raw format)
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + quote("data_by_artist.csv")
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + quote("data_by_genres (1).csv")
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + quote("data_by_year (1).csv")
DATA_W_GENRES_CSV = BASE_GITHUB_URL + quote("data_w_genres.csv")

@st.cache_data
def load_data():
    try:
        # Try reading with different encodings
        data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV, encoding='latin1', on_bad_lines='skip')
        data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV, encoding='latin1', on_bad_lines='skip')
        data_by_year = pd.read_csv(DATA_BY_YEAR_CSV, encoding='latin1', on_bad_lines='skip')
        data_w_genres = pd.read_csv(DATA_W_GENRES_CSV, encoding='latin1', on_bad_lines='skip')

        return data_by_artist, data_by_genres, data_by_year, data_w_genres

    except Exception as e:
        st.error(f"Failed to load CSV files: {str(e)}")
        st.stop()

def main():
    st.title("Music Recommendation System")

    # Load data from CSV files
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Debug: Display sample data for verification
    st.write("Sample Data by Year (Top 5 Rows):")
    st.write(data_by_year.head())

    # Inputs from the user
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    st.write(recommendations)

def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    if 'artists' not in filtered_data.columns:
        st.error("'artists' column not found in filtered data!")
        return pd.DataFrame()

    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

    return filtered_data.head(10)

if __name__ == "__main__":
    main()
