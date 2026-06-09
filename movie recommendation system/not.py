import streamlit as st
import pickle
import pandas as pd
import requests
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: 
        linear-gradient(rgba(0,0,0,0.70), rgba(0,0,0,0.70)),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("movies.jpeg")
# def fetch_poster(movie_id):
#     response=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=79abaf8f143435740eee34b4ead61c7a&language=en-US")
#     data=response.json()
#     print(data)
#     return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]
import requests

DEFAULT_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=79abaf8f143435740eee34b4ead61c7a&language=en-US"
    
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        data = response.json()

        # 🔴 movie not found
        if 'poster_path' not in data or data['poster_path'] is None:
            return DEFAULT_POSTER

        # 🟢 poster exists
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    except:
        # 🔴 network error / API error
        return DEFAULT_POSTER
def recommend(movie):
    movie_index=movies[movies["title"]==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster thrugh api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster
movies_dict=pickle.load(open("Movies_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open("Similarity.pkl","rb"))
st.markdown("<h1 style='text-align:center;'>MOVIE RECOMMENDER SYSTEM</h1>", unsafe_allow_html=True)
#st.title("MOVIE RECOMMENDER SYSTEM")
st.set_page_config(page_title="MOVIE RECOMMENDER SYSTEM",layout="wide")
#st.markdown("<h3>MOVIE RECOMMENDER SYSTEM?</h3>", unsafe_allow_html=True)

# selected_movies_name = st.selectbox(
#     "",  # keep empty label
#     movies["title"].values
# )
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown(
        "<h2 style='text-align:center;'>Search Your Movie 🎬</h2>",
        unsafe_allow_html=True
    )

    # FORM STARTS
    with st.form("movie_form"):
        selected_movies_name = st.selectbox(
            "",
            movies["title"].values
        )

        recommend_btn = st.form_submit_button("Recommend 🎥")

if recommend_btn:
    names, posters = recommend(selected_movies_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i],use_container_width=True,width=180)