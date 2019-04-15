import pandas as pd
from misc import load_pickle
from .create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import os.path
# Built using "Hands-On Recommendation Systems with Python: Start building powerful and personalized, recommendation engines with Python
# (Rounak Banik 2018)" as base frame

def generate_cosine_sim(filmsTable=None):
    if filmsTable is None:
        filmsTable = getFilmTable()

    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(filmsTable['metadata'])
    return cosine_similarity(cv_matrix, cv_matrix)

def sort_sim_scores(film_sim_scores):
    return film_sim_scores[1]

def content_recommender(FilmID, filmsTable):

    cosine_sim = generate_cosine_sim(filmsTable)

    filmIndex = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)

    film_sim_scores = list(enumerate(cosine_sim[filmIndex]))

    film_sim_scores = sorted(film_sim_scores, key=sort_sim_scores, reverse=True)[1:]

    splice = 25
    if len(film_sim_scores) < 25:
        splice = len(film_sim_scores)
    most_similar_films_indices = [pairs[0] for pairs in film_sim_scores[:splice]]

    return filmsTable.iloc[most_similar_films_indices]