import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository (ensure these paths are correct)
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres (1).csv"
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year (1).csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    # Load CSV files from GitHub
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV)
    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV)
    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV)
    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV)
    return data_by_artist, data_by_genres, data_by_year, data_w_genres

def main():
    st.title("Music Recommendation System")

    # Load data from CSV files
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    # Display the initial data (just for debugging)
    st.write("Sample Data by Year:")
    st.write(data_by_year.head())

    # Inputs from the user
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)

    # Display recommendations or warning if empty
    if not recommendations.empty:
        st.write(recommendations)
    else:
        st.warning("No recommendations found. Try selecting different filters.")

def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    st.write(f"Filtering for year: {year}, artist: {artist}, genre: {genre}")

    # Filter based on the selected year
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    st.write("Data after filtering by year:")
    st.write(filtered_data.head())  # Debug the filtered data after year filter
    
    # Check what columns exist after filtering
    st.write("Columns after filtering by year:", filtered_data.columns.tolist())

    # Handle missing columns gracefully
    if 'artists' not in filtered_data.columns:
        st.error("'artists' column not found after filtering by year!")
        st.write("Full DataFrame structure after filtering:", filtered_data.head())
        return pd.DataFrame()  # Return empty DataFrame to avoid further issues

    # Filter by artist
    filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    st.write("Data after filtering by artist:")
    st.write(filtered_data.head())  # Debugging after artist filter

    if 'genres' not in filtered_data.columns:
        st.error("'genres' column not found after filtering by artist!")
        st.write("Full DataFrame structure after artist filter:", filtered_data.head())
        return pd.DataFrame()

    # Filter by genre
    filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]
    st.write("Data after filtering by genre:")
    st.write(filtered_data.head())  # Debugging after genre filter

    if not filtered_data.empty:
        return filtered_data.head(10)
    else:
        st.warning("No recommendations found for the selected filters.")
        return pd.DataFrame()

if __name__ == "__main__":
    main()
