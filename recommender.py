import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Clean titles: remove year + lowercase
movies["clean_title"] = movies["title"].str.replace(r"\(\d{4}\)", "", regex=True)
movies["clean_title"] = movies["clean_title"].str.lower().str.strip()

# Fill missing genres
movies["genres"] = movies["genres"].fillna("")

# Vectorize genres
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Map title to index (FIRST occurrence only)
indices = {}
for i, title in enumerate(movies["clean_title"]):
    if title not in indices:
        indices[title] = i


def recommend_movies(movie_name, n=5):
    movie_name = movie_name.lower().strip()

    if movie_name not in indices:
        return ["Movie not found"]

    idx = indices[movie_name]

    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    movie_indices = [i[0] for i in scores[1:n+1]]
    return movies["title"].iloc[movie_indices].apply(remove_the).tolist()


def remove_the(title):
    # Handles: "Matrix, The (1999)"
    if ", The" in title:
        title = title.replace(", The", "")
    # Handles: "The Matrix (1999)"
    elif title.startswith("The "):
        title = title.replace("The ", "", 1)
    return title.strip()


