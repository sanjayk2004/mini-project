import pandas as pd
import streamlit as st

# Load Data Function with Error Handling
def load_data():
    st.write("Please upload your CSV files:")

    def read_csv_file(file, filename):
        try:
            return pd.read_csv(file, encoding='utf-8')  # Attempt to read with utf-8 encoding
        except UnicodeDecodeError:
            return pd.read_csv(file, encoding='latin1')  # Fallback if utf-8 fails
        except Exception as e:
            st.error(f"Error loading {filename}: {e}")
            st.stop()

    # File Uploaders
    uploaded_artist = st.file_uploader("Upload 'data_by_artist.csv'", type=["csv"])
    uploaded_genres = st.file_uploader("Upload 'data_by_genres.csv'", type=["csv"])
    uploaded_year = st.file_uploader("Upload 'data_by_year.csv'", type=["csv"])
    uploaded_w_genres = st.file_uploader("Upload 'data_w_genres.csv'", type=["csv"])

    if uploaded_artist and uploaded_genres and uploaded_year and uploaded_w_genres:
        # Read CSVs with improved error handling
        data_by_artist = read_csv_file(uploaded_artist, 'data_by_artist.csv')
        data_by_genres = read_csv_file(uploaded_genres, 'data_by_genres.csv')
        data_by_year = read_csv_file(uploaded_year, 'data_by_year.csv')
        data_w_genres = read_csv_file(uploaded_w_genres, 'data_w_genres.csv')
        return data_by_artist, data_by_genres, data_by_year, data_w_genres
    else:
        st.warning("Please upload all the required CSV files to proceed.")
        st.stop()


# Recommendation Function
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    filtered_data = data_w_genres

    # Apply filters if not "All"
    if year != "All":
        filtered_data = filtered_data[filtered_data['year'] == int(year)]
    if artist != "All":
        filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, case=False, na=False)]
    if genre != "All":
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, case=False, na=False)]

    return filtered_data[['artists', 'genres', 'year']].head(10)


# Streamlit Main App Function
def main():
    st.title("Music Recommendation System")

    # Load data after users upload the required CSV files
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()
    st.success("Files loaded successfully!")

    st.sidebar.header("Filters for Recommendation")
    year = st.sidebar.selectbox("Select Year", options=["All"] + sorted(data_by_year['year'].astype(str).unique()))
    artist = st.sidebar.text_input("Enter Artist Name", "All")
    genre = st.sidebar.text_input("Enter Genre", "All")

    if st.sidebar.button("Get Recommendations"):
        recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
        if recommendations.empty:
            st.warning("No recommendations found! Try adjusting the filters.")
        else:
            st.subheader("Top 10 Recommended Songs:")
            st.write(recommendations)


if __name__ == "__main__":
    main()
