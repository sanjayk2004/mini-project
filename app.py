import streamlit as st
import pandas as pd
import zipfile
import os

# Load and extract data
@st.cache_data
def load_data():
    base_path = "C:/Users/User/Downloads/"

    data_by_artist = pd.read_csv(base_path + "data_by_artist.csv")
    data_by_genres = pd.read_csv(base_path + "data_by_genres.csv")
    data_by_year = pd.read_csv(base_path + "data_by_year.csv")
    data_w_genres = pd.read_csv(base_path + "data_w_genres.csv")

    return data_by_artist, data_by_genres, data_by_year, data_w_genres

# Music recommendation logic
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    filtered_data = data_w_genres.copy()

    if year:
        filtered_data = filtered_data[filtered_data['year'] == int(year)]
    if artist:
        filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, case=False, na=False)]
    if genre:
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, case=False, na=False)]

    return filtered_data[['name', 'artists', 'genres', 'year']].head(10)

# Streamlit app layout
def main():
    st.title("Music Recommendation System")

    st.sidebar.header("Select your preferences")
    year = st.sidebar.text_input("Year (optional):", "")
    artist = st.sidebar.text_input("Artist (optional):", "")
    genre = st.sidebar.text_input("Genre (optional):", "")

    st.write("### Recommended Songs")
    if st.sidebar.button("Get Recommendations"):
        data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()
        recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)

        if not recommendations.empty:
            st.write(recommendations)
        else:
            st.write("No recommendations found. Try different inputs.")

if __name__ == "__main__":
    main()
