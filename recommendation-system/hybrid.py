from collaborative import collaborative_recommender
from content import content_recommender
from create_table import getFilmTable
from random import shuffle
import pandas as pd

def sort_pred_scores(film_pred_score):
    return film_pred_score[1]

def calculate_min_max(film_predictions):
    maxScore = 0
    minScore = 0
    for film in film_predictions:
        if maxScore < film[1]:
            maxScore = film[1]
        if minScore > film[1]:
            minScore = film[1]
    return maxScore, minScore

def hybrid_recommender(userId, filmID, filmsTable=None):
    if filmsTable is None:
        filmsTable = getFilmTable()
        filmsTable = filmsTable[(filmsTable['imdb_score'] > 6.29)].reset_index()
    content_result = content_recommender(filmID, filmsTable)
    collaborative_result = collaborative_recommender(userId)

    film_predictions = []
    for FilmID in content_result['FilmID']:
        film_predictions.append([FilmID, collaborative_result.predict(userId, FilmID).est])
    film_predictions.sort(key=sort_pred_scores, reverse=True)
    maxScore, minScore = calculate_min_max(film_predictions)
    if maxScore == minScore:
        shuffle(film_predictions)

    film_predictions_ids = pd.Series([film[0] for film in film_predictions[:10]])

    suggestedFilms = filmsTable[(filmsTable['FilmID'].isin(film_predictions_ids))]
    return suggestedFilms['Title']

if __name__ == '__main__':
    print(hybrid_recommender(629604219, "tt5095030"))