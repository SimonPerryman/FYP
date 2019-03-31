import pandas as pd
from reco_shared import load_pickle
from create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os.path

def get_highest_imdb_score():
    return getFilmTable().sort_values('imdb_score', ascending=False)

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

    # Measure to make sure they enter a film that exists.
    # If < 6.29 but requested, perhaps look at genres.
    filmIndex = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)

    film_sim_scores = list(enumerate(cosine_sim[filmIndex][1:]))

    film_sim_scores = sorted(film_sim_scores, key=sort_sim_scores, reverse=True)

    most_similar_films_indices = [pairs[0] for pairs in film_sim_scores[:25]]

    return filmsTable.iloc[most_similar_films_indices]