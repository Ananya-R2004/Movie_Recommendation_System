import streamlit as st
from PIL import Image
import os
import pickle
import requests

# Define paths (Ensure the logo is inside your project folder in GitHub)
logo_path = os.path.join(os.path.dirname(__file__), "images", "logo.png")
movies_path = os.path.join("MovieRec", "movies_lst.pkl")
similars_path = os.path.join("MovieRec", "smil_lst.pkl")

# Load Logo
logo = Image.open(logo_path)

# Define Colors
background_color = "#F5F5F5"  # Soft bluish-lavender for a clean and appealing look 
sidebar_bg_color = "#E0E0E0"  

# Apply background color to entire page
page_bg_css = f'''
    <style>
        .stApp {{
            background-color: {background_color};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {sidebar_bg_color};
            padding: 20px;
        }}
    </style>
'''
st.markdown(page_bg_css, unsafe_allow_html=True)

# Sidebar Content
# Sidebar Content
with st.sidebar:
    st.image(logo, width=120)
    st.markdown("""
    ## Ananya Rajesh
    **Aspiring Data Scientist | AI & ML Enthusiast**  
    Passionate about uncovering insights through data and building intelligent systems.  
    
    🎓 Pursuing Data Science Engineering  
    📍 India  
    📧 [Email](ananyarajesh2112@gmail.com)
    🌐 [GitHub](https://github.com/Ananya-R2004)  
    🌐 [LinkedIn](www.linkedin.com/in/ananya-r-a7b57b2a4) 
    
    """, unsafe_allow_html=True)
    
    st.markdown("""---""")  # Separator
    
    st.write("**About this Project:**")
    st.write(
        "This **Movie Recommendation System** helps users discover movies based on their interests. "
        "Using cutting-edge recommendation algorithms, it suggests similar movies tailored to your taste. "
        "This project showcases expertise in data science, machine learning, and user-friendly application design."
    )

# Function to Fetch Movie Poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e84f2ac078ac1ff0ecb39045772f616f&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass  # Handle errors silently
    return "https://via.placeholder.com/500x750.png?text=No+Image"  # Fallback Image

# Load Movie Data
if os.path.exists(movies_path) and os.path.exists(similars_path):
    with open(movies_path, "rb") as f:
        movies = pickle.load(f)
    with open(similars_path, "rb") as f:
        sm = pickle.load(f)
else:
    st.error("Error: Movie data files not found. Please check the paths.")
    st.stop()

# Function to Recommend Movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(sm[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for idx in distances[:10]:
        movie_id = movies.iloc[idx[0]]['movie_id']  # Get top 10 recommendations
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[idx[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

# UI Elements
st.header("Movie Recommendation System")
movie_lst = movies["title"].values
selected_movie = st.selectbox("Type or Select a movie to get recommendations", movie_lst)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display movies in 2 rows of 5
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(recommended_movie_names):
                col.text(recommended_movie_names[i + j])
                col.image(recommended_movie_posters[i + j], use_column_width=True)
