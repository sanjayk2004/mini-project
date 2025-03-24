import streamlit as st
import pandas as pd

# Load Data with File Uploader
@st.cache_data
def load_data():
    uploaded_artist = st.file_uploader("Upload 'data_by_artist.csv'", type=["csv"])
    uploaded_genres = st.file_uploader("Upload 'data_by_genres.csv'", type=["csv"])
    uploaded_year = st.file_uploader("Upload 'data_by_year.csv'", type=["csv"])
    uploaded_w_genres = st.file_uploader("Upload 'data_w_genres.csv'", type=["csv"])

    if uploaded_artist and uploaded_genres and uploaded_year and uploaded_w_genres:
        data_by_artist = pd.read_csv(uploaded_artist, encoding='latin1')
        data_by_genres = pd.read_csv(uploaded_genres, encoding='latin1')
        data_by_year = pd.read_csv(uploaded_year, encoding='latin1')
        data_w_genres = pd.read_csv(uploaded_w_genres, encoding='latin1')
        return data_by_artist, data_by_genres, data_by_year, data_w_genres
    else:
        st.warning("Please upload all required CSV files.")
        st.stop()

def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    filtered_data = data_by_year[data_by_year['year'] == int(year)]

    if not filtered_data.empty:
        artist_based = data_by_artist[data_by_artist['artists'].str.contains(artist, case=False, na=False)]
        genre_based = data_by_genres[data_by_genres['genres'].str.contains(genre, case=False, na=False)]

        recommendations = pd.concat([filtered_data, artist_based, genre_based]).drop_duplicates()
        return recommendations[['artists', 'genres', 'danceability', 'energy', 'valence', 'popularity']]
    else:
        st.warning(f"No data available for the year {year}.")
        return pd.DataFrame()

# Streamlit Main App Function
def main():
    st.title("Music Recommendation System")
    st.write("Upload the necessary CSV files and get music recommendations based on year, artist, and genre.")

    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()

    year = st.text_input("Enter Year (e.g., 2000)")
    artist = st.text_input("Enter Artist Name (optional)")
    genre = st.text_input("Enter Genre (optional)")

    if st.button("Recommend Music"):
        if year.isdigit():
            recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
            if not recommendations.empty:
                st.write("### Recommended Tracks:")
                st.dataframe(recommendations)
        else:
            st.error("Please enter a valid year.")

if __name__ == '__main__':
    main()
