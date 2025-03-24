import pandas as pd
import streamlit as st

# URLs for the CSV files (direct GitHub raw links)
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres%20(1).csv"
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year%20(1).csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    # Load CSVs with standardized column formatting
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV, encoding='ISO-8859-1')
    data_by_artist.columns = data_by_artist.columns.str.strip().str.lower()  # Normalize columns

    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV, encoding='ISO-8859-1')
    data_by_genres.columns = data_by_genres.columns.str.strip().str.lower()

    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV, encoding='ISO-8859-1')
    data_by_year.columns = data_by_year.columns.str.strip().str.lower()

    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV, encoding='ISO-8859-1')
    data_w_genres.columns = data_w_genres.columns.str.strip().str.lower()

    return data_by_artist, data_by_genres, data_by_year, data_w_genres

def main():
    st.title("Music Recommendation System")

    # Load data
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Debugging Step: Print available column names in each DataFrame
    st.write("Columns in 'data_by_artist':", data_by_artist.columns.tolist())
    st.write("Columns in 'data_by_year':", data_by_year.columns.tolist())

    # User Inputs
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())  # Expecting 'artists' in column names
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    st.write(recommendations)

def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    
    # Handling potential issues with columns, apply debugging checks:
    if 'artists' not in filtered_data.columns:
        st.error("'artists' column not found in filtered data!")
        return pd.DataFrame()  # Return empty DataFrame if column is missing
    
    # Filter data based on user selections
    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

    # Return top 10 recommendations
    return filtered_data.head(10)

if __name__ == "__main__":
    main()
