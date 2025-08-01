import streamlit as st
import pandas as pd
import gzip, pickle, os, requests
from fuzzywuzzy import process
import matplotlib.pyplot as plt

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Movie Recs", layout="wide")
st.markdown("""
<style>
  section[data-testid="stSidebar"] { background: #DDDDDD; padding:20px; }
  .stApp { background: #F4F4F4; }
  .dark-mode { background: #1e1e1e; color: #eee; }
  div.stButton > button { background:white!important; color:black!important; }
</style>
""", unsafe_allow_html=True)

# --- DARK MODE TOGGLE ---
dark = st.sidebar.checkbox("🌙 Dark Mode")
if dark: st.markdown('<body class="dark-mode">', unsafe_allow_html=True)

# --- SIDEBAR INFO ---
with st.sidebar:
    st.image("images/logo.png", width=100, caption="Ananya R")
    st.markdown("""
    ## Ananya R  
    Aspiring Data Scientist | AI & ML Enthusiast  
    🎓 Data Science Engineering  
    📍 India  
    """)
    st.markdown("---")
    st.markdown("📝 [Medium](https://medium.com/@ananyarajesh2112)")

# --- LOAD MOVIE DATA ---
@st.cache_data
def load_data():
    # you should have movies_lst_compressed.pkl.gz and smil_lst_compressed.pkl.gz
    with gzip.open("MovieRec/movies_lst_compressed.pkl.gz",'rb') as f:
        movies = pickle.load(f)
    with gzip.open("MovieRec/smil_lst_compressed.pkl.gz",'rb') as f:
        sm = pickle.load(f)
    return movies, sm

movies, sm = load_data()

# --- SEARCH BAR + RATING FILTER ---
st.title("🎬 Movie Recommendation System")
query = st.text_input("🔍 Search for a movie title")
min_rating = st.slider("⭐ Minimum IMDb Rating", 0.0, 10.0, 5.0, 0.5)

# --- UTILS: POSTER + TRAILER ---
API_KEY = "YOUR_TMDB_API_KEY"
def fetch_poster(id):
    try:
        data = requests.get(
            f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}"
        ).json()
        return "https://image.tmdb.org/t/p/w200" + data["poster_path"]
    except: return ""

def fetch_trailer(id):
    url = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={API_KEY}"
    for v in requests.get(url).json().get("results", []):
        if v["site"]=="YouTube" and v["type"]=="Trailer":
            return "https://youtu.be/" + v["key"]
    return None

# --- FUZZY SEARCH & RECOMMEND ---
def get_index(title):
    match, score = process.extractOne(title, movies['title'])
    return movies.index[movies['title']==match][0] if score>60 else None

def recommend(idx):
    sims = sorted(list(enumerate(sm[idx])), key=lambda x: x[1], reverse=True)[1:11]
    recs = []
    for i,_ in sims:
        row = movies.iloc[i]
        if row.vote_average >= min_rating:
            recs.append({
                "title": row.title,
                "rating": row.vote_average,
                "poster": fetch_poster(row.movie_id),
                "trailer": fetch_trailer(row.movie_id)
            })
    return recs

if query:
    idx = get_index(query)
    if idx is None:
        st.warning("No close match found.")
    else:
        st.subheader(f"Because you searched for **{movies.iloc[idx].title}**")
        recs = recommend(idx)
        for movie in recs:
            cols = st.columns([1,3,1])
            cols[0].image(movie["poster"])
            cols[1].markdown(f"**{movie['title']}**  \n⭐ {movie['rating']}")
            if movie["trailer"]:
                cols[2].markdown(f"[▶️ Trailer]({movie['trailer']})")

# --- ANALYTICS TAB ---
with st.expander("📊 Genre Analytics"):
    genre_dummies = movies['genres'].str.get_dummies(sep='|')
    top10 = genre_dummies.sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    top10.plot.bar(ax=ax)
    ax.set_ylabel("Count")
    st.pyplot(fig)

# --- FOOTER ---
st.markdown(
    "<div style='text-align:center;padding:10px;'>"
    "Developed with ❤️ by Ananya Rajesh | Data from TMDB"
    "</div>", unsafe_allow_html=True
)
