import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(layout="wide")
THEME_COLOR = "#1F1F1F"
ACCENT_COLOR = "#E50914"

st.markdown(
    f"""
    <style>
        .css-18e3th9 {{
            background-color: {THEME_COLOR};
        }}
        .stButton>button {{
            color: {THEME_COLOR};
            background-color: {ACCENT_COLOR};
            position: sticky;
            top: 0;
            z-index: 1;
        }}
        .stTextInput>div>div>input {{
            color: {THEME_COLOR};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Movie Recommender System", anchor=None)

select_value = st.text_input("Type the movie name", "", help="Enter a movie name to get similar recommendations.")

def fetch_posters(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ee0494637aebb47deadab3e577ff8db1&language=en-US'
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        poster_path = data['poster_path']
        if poster_path:
            full_path = 'https://image.tmdb.org/t/p/w500' + poster_path
            return full_path
    return None

def recommend(movie):
    movie = movie.lower()
    index = None
    try:
        index = movies[movies['title'].str.lower() == movie].index[0]
    except IndexError:
        pass
    
    if index is not None:
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommend_movie = []
        recommend_poster = []
        for i in distance[0:5]:
            movie_id = movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            recommend_poster.append(fetch_posters(movie_id))
        return recommend_movie, recommend_poster
    else:
        st.error("Movie not found.")
        return None


if st.button('Show Recommendations'):
    if select_value:
        recommendation = recommend(select_value)
        if recommendation is not None:
            movie_name, movie_poster = recommendation
            num_cols = 5
            cols = st.columns(num_cols)

            for i in range(min(num_cols, len(movie_name))):
                with cols[i]:
                    st.text(movie_name[i])
                    st.image(movie_poster[i], use_column_width='always')
        else:
            st.warning("No recommendations found for the entered movie name.")
    else:
        st.info("Please type a movie name to get recommendations.")
