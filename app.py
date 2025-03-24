import pandas as pd
import streamlit as st

# URLs of the CSV files in your GitHub repository
BASE_GITHUB_URL = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/"
DATA_BY_ARTIST_CSV = BASE_GITHUB_URL + "data_by_artist.csv"
DATA_BY_GENRES_CSV = BASE_GITHUB_URL + "data_by_genres (1).csv"
DATA_BY_YEAR_CSV = BASE_GITHUB_URL + "data_by_year (1).csv"
DATA_W_GENRES_CSV = BASE_GITHUB_URL + "data_w_genres.csv"

@st.cache_data
def load_data():
    data_by_artist = pd.read_csv(DATA_BY_ARTIST_CSV)
    data_by_genres = pd.read_csv(DATA_BY_GENRES_CSV)
    data_by_year = pd.read_csv(DATA_BY_YEAR_CSV)
    data_w_genres = pd.read_csv(DATA_W_GENRES_CSV)
    return data_by_artist, data_by_genres, data_by_year, data_w_genres

def main():
    st.title("Music Recommendation System")

    # Load data from the cached function
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()
    
    st.write("Data Loaded Successfully!")
    
    # Display sample data to check
    st.write("Sample data (data_by_year):", data_by_year.head())
    
    # Inputs from the user
    year = st.selectbox("Select Year", data_by_year['year'].unique())
    artist = st.selectbox("Select Artist", data_by_artist['artists'].unique())
    genre = st.selectbox("Select Genre", data_by_genres['genres'].unique())

    st.write("### Recommended Songs Based on Your Inputs:")
    recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
    
    # Display recommendations or a warning if empty
    if not recommendations.empty:
        st.write(recommendations)
    else:
        st.warning("No recommendations found. Try selecting different filters.")

# Music Recommendation Logic
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    # Step 1: Filter based on the selected year
    filtered_data = data_by_year[data_by_year['year'] == int(year)]
    st.write("After filtering by year:", filtered_data.columns)
    
    # Step 2: Ensure the artists column exists before filtering by artist
    if 'artists' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, na=False)]
    else:
        st.error("'artists' column not found in filtered data after filtering by year!")
        return pd.DataFrame()  # Return empty DataFrame to prevent further errors

    st.write("After filtering by artist:", filtered_data.columns)

    # Step 3: Filter by genre and check the DataFrame again
    if 'genres' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, na=False)]
    else:
        st.error("'genres' column not found in filtered data after filtering by artist!")
        return pd.DataFrame()  # Return empty DataFrame to prevent further errors
    
    st.write("After filtering by genre:", filtered_data.columns)

    # Step 4: Return top recommendations (10 rows)
    if not filtered_data.empty:
        return filtered_data.head(10)
    else:
        st.warning("No recommendations found for the selected criteria.")
        return pd.DataFrame()

if __name__ == "__main__":
    main()
