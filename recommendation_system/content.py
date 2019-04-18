import pandas as pd
from misc import load_pickle
from .create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import os.path
# Built using "Hands-On Recommendation Systems with Python: Start building powerful and personalized, recommendation engines with Python
# (Rounak Banik 2018)" as base frame

def generate_cosine_sim(filmsTable=None):
    """Generates a cosine similarity matrix using the count vectorizer.
    @param {Pandas DataFrame} filmsTable
    @returns {Object} cosine_similarity - cosine similarity matrix"""
    if filmsTable is None:
        filmsTable = getFilmTable()

    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(filmsTable['metadata'])
    return cosine_similarity(cv_matrix, cv_matrix)

def sort_sim_scores(film_sim_scores):
    """Sorts the film score based on its score.
    @param {Pandas Series} film_sim_scores
    @returns the score"""
    return film_sim_scores[1]

def content_recommender(FilmID, filmsTable):
    """Generates the top 25 most similar films to a given film.
    If less than 25 films present, returns all films, sorted in similarity order.
    @param {String} FilmID
    @param {Pandas DataFrame} filmsTable
    @returns {Pandas DataFrame} filmsTable (reduced to the 25th most similar films)"""

    cosine_sim = generate_cosine_sim(filmsTable)

    filmIndex = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)

    film_sim_scores = list(enumerate(cosine_sim[filmIndex]))

    film_sim_scores = sorted(film_sim_scores, key=sort_sim_scores, reverse=True)[1:]

    splice = 25
    if len(film_sim_scores) < 25:
        splice = len(film_sim_scores)
    most_similar_films_indices = [pairs[0] for pairs in film_sim_scores[:splice]]

    return filmsTable.iloc[most_similar_films_indices]