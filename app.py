import pandas as pd
import streamlit as st

# Load Data Function
def load_data():
    st.write("Please upload your CSV files:")
    
    # File Uploaders for CSVs
    uploaded_artist = st.file_uploader("Upload 'data_by_artist.csv'", type=["csv"])
    uploaded_genres = st.file_uploader("Upload 'data_by_genres.csv'", type=["csv"])
    uploaded_year = st.file_uploader("Upload 'data_by_year.csv'", type=["csv"])
    uploaded_w_genres = st.file_uploader("Upload 'data_w_genres.csv'", type=["csv"])

    if uploaded_artist and uploaded_genres and uploaded_year and uploaded_w_genres:
        # Read CSVs with encoding handling
        data_by_artist = pd.read_csv(uploaded_artist, encoding='latin1')
        data_by_genres = pd.read_csv(uploaded_genres, encoding='latin1')
        data_by_year = pd.read_csv(uploaded_year, encoding='latin1')
        data_w_genres = pd.read_csv(uploaded_w_genres, encoding='latin1')
        return data_by_artist, data_by_genres, data_by_year, data_w_genres
    else:
        st.warning("Please upload all the required CSV files to proceed.")
        st.stop()


# Recommendation Function
def recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres):
    # Filter data based on year, artist, and genre
    filtered_data = data_w_genres

    if year != "All":
        filtered_data = filtered_data[filtered_data['year'] == int(year)]
    if artist != "All":
        filtered_data = filtered_data[filtered_data['artists'].str.contains(artist, case=False, na=False)]
    if genre != "All":
        filtered_data = filtered_data[filtered_data['genres'].str.contains(genre, case=False, na=False)]
    
    # Return top 10 recommendations
    return filtered_data[['artists', 'genres', 'year']].head(10)


# Streamlit Main App Function
def main():
    st.title("Music Recommendation System")

    # Load data with file uploaders
    data_by_artist, data_by_genres, data_by_year, data_w_genres = load_data()
    st.success("Files loaded successfully!")

    st.sidebar.header("Filters for Recommendation")
    
    # Sidebar options
    year = st.sidebar.selectbox("Select Year", options=["All"] + sorted(data_by_year['year'].astype(str).unique()))
    artist = st.sidebar.text_input("Enter Artist Name", "All")
    genre = st.sidebar.text_input("Enter Genre", "All")

    # Button to get recommendations
    if st.sidebar.button("Get Recommendations"):
        recommendations = recommend_music(year, artist, genre, data_by_year, data_by_artist, data_by_genres, data_w_genres)
        
        if recommendations.empty:
            st.warning("No recommendations found! Try adjusting the filters.")
        else:
            st.subheader("Top 10 Recommended Songs:")
            st.write(recommendations)


if __name__ == "__main__":
    main()
