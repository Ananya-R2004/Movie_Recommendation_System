import streamlit as st
from PIL import Image
import os
import pickle
import requests
import gzip

# Define paths
logo_path = os.path.join(os.path.dirname(__file__), "images", "logo.png")
movies_path = os.path.join("MovieRec", "movies_lst_compressed.pkl.gz")
similars_path = os.path.join("MovieRec", "smil_lst_compressed.pkl.gz")

# Load logo if available
try:
    logo = Image.open(logo_path)
except FileNotFoundError:
    logo = None


custom_css = """
    <style>
        [data-testid="stSidebar"] > div:first-child {
            background-color: #DDDDDD;
            padding: 20px;
            border-right: 1px solid #CCCCCC;
        }

        .stApp {
            background-color: #F4F4F4;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Content
with st.sidebar:
    if logo:
        st.image(logo, width=120)
    st.markdown("""
    ## Ananya R
    **Aspiring Data Scientist | AI & ML Enthusiast**  
    Passionate about uncovering insights through data and building intelligent systems.  
    
    🎓 Pursuing Data Science Engineering  
    📍 India  
    📧 [Email](mailto:ananyarajesh2112@gmail.com)  
    🌐 [GitHub](https://github.com/Ananya-R2004)  
    🌐 [LinkedIn](https://www.linkedin.com/in/ananya-r-a7b57b2a4)
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.write("**About this Project:**")
    st.write(
        "This **Movie Recommendation System** helps users discover movies based on their interests. "
        "Using cutting-edge recommendation algorithms, it suggests similar movies tailored to your taste. "
        "This project showcases expertise in data science, machine learning, and user-friendly application design."
    )

    st.markdown("""
    ---
    📝 [Medium](https://medium.com/@ananyarajesh2112)  
    *Explore my technical journey & project documentation here.*
    """, unsafe_allow_html=True)

# Function to Fetch Poster
def fetch_poster(movie_id):
    api_key = "e84f2ac078ac1ff0ecb39045772f616f"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/500x750.png?text=No+Image"

# Load Movie Data
if os.path.exists(movies_path) and os.path.exists(similars_path):
    try:
        with gzip.open(movies_path, 'rb') as f:
            movies = pickle.load(f)
        with gzip.open(similars_path, 'rb') as f:
            sm = pickle.load(f)
    except Exception as e:
        st.error(f"Error loading movie data: {e}")
        st.stop()
else:
    st.error("Error: Movie data files not found. Please check the paths.")
    st.stop()

# Recommendation Logic
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(sm[index])), reverse=True, key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []
        for idx in distances[1:11]:
            movie_id = movies.iloc[idx[0]]['movie_id']
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[idx[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        st.error("Selected movie not found. Please choose another.")
        return [], []

# Main Interface
st.markdown("<h1 style='font-size: 40px;'>Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("Type or Select a movie to get Movie Recommendation")

movie_lst = movies["title"].values
selected_movie = st.selectbox("", movie_lst)

# Button Styling (white background, black border)
button_css = """
    <style>
        div.stButton > button {
            background-color: white !important;
            color: black !important;
            border: 1px solid #999999 !important;
            padding: 0.5em 1em;
            font-weight: bold;
            border-radius: 6px;
        }
        div.stButton > button:hover {
            background-color: #A8A8A8 !important;
            border: 1px solid #666666 !important;
        }
    </style>
"""
st.markdown(button_css, unsafe_allow_html=True)

# Show Recommendations
if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        for i in range(0, len(recommended_movie_names), 5):
            cols = st.columns(5)
            for j, col in enumerate(cols):
                if i + j < len(recommended_movie_names):
                    col.text(recommended_movie_names[i + j])
                    col.image(recommended_movie_posters[i + j], use_column_width=True)
    else:
        st.warning("No recommendations found.")
