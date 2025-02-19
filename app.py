import streamlit as st
from PIL import Image
import base64
import pandas as pd
import pickle
import requests

# Define paths
logo_path = "C:\\Users\\ananya\\Pictures\\MRS\\images\\logo.png"

# Define Colors
background_color = "#F5F5F5   "  # Soft bluish-lavender for a clean and appealing look
sidebar_bg_color = "#E0E0E0   "  # Thistle shade for a modern, sophisticated touch

# Load Logo
logo = Image.open(logo_path)

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

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=e84f2ac078ac1ff0ecb39045772f616f&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(sm[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[0:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.header("Movie Recommendation System")
movies=pickle.load(open(r"C:\\Users\\ananya\\Pictures\\MRS\\MovieRec\\movies_lst.pkl","rb"))
sm=pickle.load(open(r"C:\\Users\\ananya\\Pictures\\MRS\\MovieRec\\smil_lst.pkl","rb"))

movie_lst=movies["title"].values
selected_movie=st.selectbox(
    "Type or Select a movie to get Movie Recommendation",
    movie_lst
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    row1 = st.columns(5)
    row2 = st.columns(5)
    
    # Fill the first row (first 5 recommendations)
    for idx, col in enumerate(row1):
        col.text(recommended_movie_names[idx])
        col.image(recommended_movie_posters[idx])
    
    # Fill the second row (next 5 recommendations)
    for idx, col in enumerate(row2):
        col.text(recommended_movie_names[idx + 5])
        col.image(recommended_movie_posters[idx + 5])
