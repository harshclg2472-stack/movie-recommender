import streamlit as st
from recommender import recommend_movies

# Page config
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
.card {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    font-size: 18px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# Title
st.title("🎬 Movie Recommendation System")
st.caption("An easier way for you to search unexplored and watch worthy movies")
st.divider()

with st.sidebar:
    st.header("ℹ Project Info")
 
    mood = st.selectbox(
        "🎭 Choose your mood",
        ["Any", "Happy 😊", "Romantic ❤️", "Action 💥", "Thriller 😱"]
    )

# Search box
movie_name = st.text_input(
    "🔍 Search for a movie",
    placeholder="Type a movie name (e.g. Titanic, Toy Story)"
)

# Button
if st.button("🎯 Recommend"):
    if movie_name.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        with st.spinner("Finding similar movies..."):
            try:
                recommendations = recommend_movies(movie_name)

                if recommendations:
                    st.subheader("✨ Recommended Movies")
                    for movie in recommendations:
                        st.markdown(f"🎥 **{movie}**")
                else:
                    st.info("No similar movies found.")

            except:
                st.error("Movie not found. Please check spelling.")
