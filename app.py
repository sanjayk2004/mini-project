import streamlit as st
import pandas as pd
from time import sleep
 

@st.cache_data  
def load_data():
    try:
        dataset_urls = [
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/tcc_ceds_music.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Hindi_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Malayalam_songs.csv",
            "https://raw.githubusercontent.com/sanjayk2004/mini-project/main/Tamil_songs.csv"
        ]

        combined_data = pd.DataFrame()
        progress_text = st.empty()  
        progress_bar = st.progress(0)  

        for i, url in enumerate(dataset_urls):
            progress_text.text(f"Loading dataset {i + 1} of {len(dataset_urls)}...")
            progress_bar.progress((i + 1) / len(dataset_urls))  
            try:
                data = pd.read_csv(url)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
            except Exception as e:
                st.error(f"Failed to load dataset {i + 1}: {url}")
                st.error(f"Error details: {e}")
                continue

        progress_text.text("All datasets loaded successfully!")
        return combined_data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

# Function to filter and recommend music
def recommend_music(release_date, artist, genre, data):
    if data is None:
        st.error("No data available to process recommendations.")
        return "No data available."

    
    filtered_data = data.copy()

 
    if release_date:
        try:
            filtered_data = filtered_data[filtered_data['release_date'] == int(release_date)]
        except (KeyError, ValueError):
            st.warning("Invalid or missing 'release_date' column/inputs.")

  
    if artist and 'artist_name' in filtered_data.columns:
        filtered_data['artist_name'] = filtered_data['artist_name'].astype(str)
        filtered_data = filtered_data[filtered_data['artist_name'].str.contains(artist, case=False, na=False)]

 
    if genre and 'genre' in filtered_data.columns:
        filtered_data['genre'] = filtered_data['genre'].astype(str)
        filtered_data = filtered_data[filtered_data['genre'].str.contains(genre, case=False, na=False)]

   
    if filtered_data.empty:
        return "No recommendations found for the given inputs."

   
    available_columns = [col for col in ['track_name', 'artist_name', 'genre', 'release_date'] if col in filtered_data.columns]
    return filtered_data[available_columns].head(100)

def main():
 
    st.set_page_config(
        page_title="🎵 Music Recommendation System",
        page_icon="🎵",
        layout="wide"
    )


    st.markdown(
        """
        <style>
        .stApp {
            background: #87CEEB; /* Sky Blue background */
            color: #333333; /* Dark gray text */
        }
        h1 {
            font-family: 'Poppins', sans-serif;
            text-align: center;
            color: #333333; /* Dark gray heading */
        }
        .sidebar .sidebar-content {
            background: #ffffff; /* White sidebar background */
            color: #333333; /* Dark gray text */
        }
        .stButton>button {
            background-color: #ff9900; /* Orange button */
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
        }
        /* Style for the GitHub link */
        a {
            color: #333333 !important; /* Dark gray link */
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🎵 Music Recommendation System 🎵")

    data = load_data()

    if data is None:
        st.error("Failed to load datasets. Please check the logs for more details.")
        return


    st.sidebar.subheader("🎵 Enter Your Preferences")
    with st.sidebar.form(key="recommendation_form"):
        release_date = st.text_input("Release Date:")
        artist = st.text_input("Artist Name:")
        genre = st.text_input("Genre:")

        # Submit button with "Enter" key support
        submit_button = st.form_submit_button(label="Get Recommendations")

    if submit_button:
        if not (release_date or artist or genre):
            st.warning("Please enter at least one filter (Release Date, Artist, or Genre).")
        else:
            recommendations = recommend_music(release_date, artist, genre, data)

            # Display the recommendations in the main area
            st.subheader("🎶 Recommendations")
            if isinstance(recommendations, pd.DataFrame):
                # Apply custom styling to the table
                styled_table = (
                    recommendations.style
                    .set_properties(**{
                        'background-color': '#ffffff',  
                        'color': '#333333',             
                        'border-color': '#cccccc'
                    })
                    .set_table_styles([
                        {
                            'selector': 'th',
                            'props': [('background-color', '#87CEEB'), ('color', 'white')]  
                        },
                        {
                            'selector': 'td',
                            'props': [('color', '#333333')]  
                        }
                    ])
                )
                st.table(styled_table)
            else:
                st.info(recommendations)

  
    with st.expander("ℹ️ How to Use This App"):
        st.write("""
        1. Enter your preferences in the sidebar (e.g., Release Date, Artist, Genre).
        2. Press "Get Recommendations" or hit the "Enter" key.
        3. View up to 100 song recommendations based on your inputs.
        """)


    with st.expander("📊 Dataset Details"):
        st.write("""
        This app combines data from multiple datasets:
        - tcc_ceds_music.csv
        - Hindi_songs.csv
        - Malayalam_songs.csv
        - Tamil_songs.csv
        """)
        
if __name__ == "__main__":
    main()
