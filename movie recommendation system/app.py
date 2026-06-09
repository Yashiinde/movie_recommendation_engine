import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=79abaf8f143435740eee34b4ead61c7a&language=en-US")
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]
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
selected_movies_name=st.selectbox(
    "which movie you would like to watch ?",
    movies["title"].values
)
if st.button("Recommend"):
    names,posters = recommend(selected_movies_name)
    cols = st.columns(5)  # create 5 columns
    for i, col in enumerate(cols):
        col.markdown(f"<p style='font-size:20px; text-align:center'>{names[i]}</p>", unsafe_allow_html=True)
        col.image(posters[i], use_container_width=True, width=180)
#     col1,col2,col3,col4,col5=st.columns(5)

#     cols = [col1, col2, col3, col4, col5]

# for i, col in enumerate(cols):
#     col.markdown(f"<p style='font-size:14px; text-align:center'>{names[i]}</p>", unsafe_allow_html=True)
#     col.image(posters[i])
    # with col1:
    #     st.subheader(names[0])
    #     st.image(poster[0])
    # with col2:
    #     st.subheader(names[1])
    #     st.image(poster[1])
    # with col3:
    #     st.subheader(names[2])
    #     st.image(poster[2])   
    # with col4:
    #     st.subheader(names[3])
    #     st.image(poster[3])
    # with col5:
    #     st.subheader(names[4])
    #     st.image(poster[4])   
    # for i in recommendation:
    #     st.write(i)