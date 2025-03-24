import pandas as pd
import streamlit as st

# Updated URLs with correct filenames
DATA_BY_ARTIST_CSV = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/data_by_artist.csv"
DATA_BY_GENRES_CSV = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/data_by_genres.csv"
DATA_BY_YEAR_CSV = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/data_by_year.csv"
DATA_W_GENRES_CSV = "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/data_w_genres.csv"

@st.cache_data
def load_data():
    try:
        # Load CSVs with encoding to avoid Unicode errors
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
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()
    st.write("Sample Data by Year (Top 5 Rows):")
    st.write(data_by_year.head())

if __name__ == "__main__":
    main()
