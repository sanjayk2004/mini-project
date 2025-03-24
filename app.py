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

    if any(df is None or df.empty for df in [data_by_artist, data_by_genres, data_by_year, data_w_genres]):
        st.error("Data could not be loaded or is empty. Please check your CSV files.")
        return

    # Artist selection now strictly based on `data_by_artist`
    st.write("Columns in data_by_artist dataset:", data_by_artist.columns)
    artist = st.selectbox("Select Artist", sorted(data_by_artist['artists'].dropna().unique())) if 'artists' in data_by_artist.columns else None
    year = st.selectbox("Select Year", sorted(data_by_year['year'].dropna().unique())) if 'year' in data_by_year.columns else None
    genre = st.selectbox("Select Genre", sorted(data_by_genres['genres'].dropna().unique())) if 'genres' in data_by_genres.columns else None

    if not (artist and year and genre):
        st.error("Please ensure 'artist', 'year', and 'genre' are correctly selected.")
        return

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, genre, data_by_year, data_by_genres)
    st.write(recommendations)

def recommend_music(year, genre, data_by_year, data_by_genres):
    try:
        # Filter by year and genre (skipping artist filtering here)
        filtered_data = data_by_year[data_by_year['year'] == int(year)]
        st.write("Columns in filtered_data after filtering by year:", filtered_data.columns)

        # Now filter with genres
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]

        if filtered_data.empty:
            return "No matching songs found based on your filters."
        
        # Display top 10 songs from the filtered dataset
        return filtered_data.head(10)
    except Exception as e:
        return f"Error during filtering: {e}"

if __name__ == "__main__":
    main()
