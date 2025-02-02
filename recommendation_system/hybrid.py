"""
Hybrid recommender file
"""

from .collaborative import collaborative_recommender
from .content import content_recommender
from .create_table import getFilmTable
from random import shuffle, randint
import pandas as pd
import sys
import os
sys.path.insert(0, os.environ['APPLICATION_PATH'])
from database import getQueryInfo, getUserRatings

def sort_by_highest_imdb_score(filmsTable=None):
    """Sorts the filmsTable by imdb score
    @param {DataFrame} filmsTable
    @returns {DataFrame} filmsTable sorted by imdb score"""
    if filmsTable is None:
        filmsTable = getFilmTable()
    return filmsTable.sort_values('imdb_score', ascending=False)

def sort_pred_scores(film_pred_score):
    """Sorts the predicted films by their score
    @param {List} film_pred_score - predicted score for a film
    @returns {Int} predicted film score"""
    return film_pred_score[1]

def calculate_min_max(film_predictions):
    """Calculate the minimum and max scores of the predicted films
    @param {List} film_predictions - predicted film scores for the user
    @returns {Int} maxScore
    @returns {Int} minScore"""
    maxScore = 0
    minScore = 0
    for film in film_predictions:
        if maxScore < film[1]:
            maxScore = film[1]
        if minScore > film[1]:
            minScore = film[1]
    return maxScore, minScore

def find_films_with_user_query(requested_data, film_data):
    """Finds films with specific data, e.g. films for a specific genre.
    @param {List} requested_data - user requested data items, e.g. 'comedy', 'nm123456', 'tt123456'
    @param {List} film_data - Film Data
    @returns True if found, else False
    """
    for data in requested_data:
        if data in film_data:
            return True
    return False

def find_films_with_all_genres(requested_genres, film_genres):
    """Function to find films that have all of the requested genres in it.
    @param {List} requested_genres
    @param {List} film_genres
    @returns True if all of requested_genres are in film_genres, else False"""
    counter = 0
    for genre in requested_genres:
        if genre in film_genres:
            counter = counter + 1
    if counter == len(requested_genres):
        return True
    return False

def get_generated_requested_filmID(UserID, filmsTable):
    """Function to generate a random film ID, either from the user's known liked films,
    or from the IMDB top 250.
    @param {Int} UserID
    @param {DataFrame} filmsTable
    @returns {String} randomly generated filmID"""
    db_query = getUserRatings(UserID)
    user_ratings = []
    if db_query:
        user_ratings = [rating['FilmID'] for rating in db_query if rating['Liked'] == 1]
    if not user_ratings:
        user_ratings = sort_by_highest_imdb_score(filmsTable).reset_index(drop=True)[:250]
        user_ratings = user_ratings['FilmID'].tolist()
    shuffle(user_ratings)
    index = randint(0, len(user_ratings) - 1)
    return user_ratings[index]
    
def create_combined_film(requested_FilmIDs, filmsTable):
    """Creates a film and relevant metadata by combining multiple films
    @param {List} requested_FilmIDs
    @param {Pandas DataFrame} filmsTable
    @returns {Int} requested_FilmID, {Pandas DataFrame} filmsTable"""
    filmsTable = getFilmTable()
    combined_directors = set()
    combined_writers = set()
    combined_crew = set()
    combined_genres = set()
    for filmID in requested_FilmIDs:
        film = filmsTable[(filmsTable['FilmID'] == filmID)]
        directors = film['Directors'].tolist()
        if directors:
            for director in directors[0]:
                combined_directors.add(director)
        writers = film['Writers'].tolist()
        if writers:
            for writers in writers[0]:
                combined_writers.add(writers)
        crew_members = film['CrewID'].tolist()
        if crew_members:
            for crew_member in crew_members[0]:
                combined_crew.add(crew_member)
        genres = film['Genres'].tolist()
        if genres:
            for genre in genres[0]:
                combined_genres.add(genre)
    combined_directors = list(combined_directors)
    combined_writers = list(combined_writers)
    combined_crew = list(combined_crew)
    combined_genres = list(combined_genres)
    metadata = '{} {} {}'.format(' '.join(combined_genres), ' '.join(list(set(combined_writers + combined_directors))), ' '.join(combined_crew))
    filmsTable.loc[filmsTable.shape[0]] = [
        "CombinedFilmID", "Combined Film", 0, None, None, combined_genres, None, None, combined_writers, combined_directors, combined_crew, 0, 0, 0, metadata
        ]
    return "CombinedFilmID", filmsTable

def build_tailored_films_table(User):
    """Build a films table tailored to the user's requests
    @param {Person} User
    @returns {DataFrame} filmsTable
    @returns {String} requested_filmIDs
    @returns {List} requested_film_indices - List of Ints. Indicies of original
                                             requested films (for when there are
                                             multiple films requested)"""
    filmsTable = getFilmTable()
    query_info = getQueryInfo(User.id)
    requested_filmIDs = []
    requested_genres = []
    requested_crew = []
    for result in query_info:
        if result['Type'] == 1:
            requested_filmIDs.append(result['Information'])
        elif result['Type'] == 2:
            requested_genres.append(result['Information'])
        elif result['Type'] == 3:
            requested_crew.append(result['Information'])

    # Removed any potential incorrect values
    requested_filmIDs = [requested_filmID for requested_filmID in requested_filmIDs if requested_filmID.startswith("tt")]

    # Store copy of requested Film IDs
    original_requested_filmIDs = requested_filmIDs

    # Combine requested films metadata
    if requested_filmIDs:
        if len(requested_filmIDs) > 1:
            requested_filmIDs, filmsTable = create_combined_film(requested_FilmIDs, filmsTable) 
        else:
            requested_filmIDs = ''.join(requested_filmIDs)
    
    # No Film Selected
    if not requested_filmIDs:
        requested_filmIDs = get_generated_requested_filmID(User.id, filmsTable)
        original_requested_filmIDs = [requested_filmIDs]
      
    # No Genres Selected
    if not requested_genres:
        if User.favouriteGenre:
            requested_genres.append(User.favouriteGenre)
        if User.secondFavouriteGenre:
            requested_genres.append(User.secondFavouriteGenre)
        if User.thirdFavouriteGenre:
            requested_genres.append(User.thirdFavouriteGenre)

    #TODO (Future) - Check for exact film requirements
    # exactFilmsTable = filmsTable[(
    #         ((filmsTable['Writers'].apply(lambda writers: find_films_with_user_query(requested_crew, writers) if requested_crew else True) |
    #         filmsTable['Directors'].apply(lambda directors: find_films_with_user_query(requested_crew, directors) if requested_crew else True) |
    #         filmsTable['CrewID'].apply(lambda crew: find_films_with_user_query(requested_crew, crew) if requested_crew else True)) &
    #         filmsTable['Genres'].apply(lambda genre: find_films_with_all_genres(requested_genres, genre) if requested_genres else True)) &
    #         (filmsTable['isAdult'].apply(lambda isAdult: False if (User.age < 18 and isAdult == 1) else True))
    #         )]
    # if exactFilmsTable.shape[0] != 0:
    #     return (0, exactFilmsTable['Title'])
    
    # differentGenresFilmTable = filmsTable[(
    #         ((filmsTable['Writers'].apply(lambda writers: find_films_with_user_query(requested_crew, writers) if requested_crew else True) |
    #         filmsTable['Directors'].apply(lambda directors: find_films_with_user_query(requested_crew, directors) if requested_crew else True) |
    #         filmsTable['CrewID'].apply(lambda crew: find_films_with_user_query(requested_crew, crew) if requested_crew else True)) &
    #         filmsTable['Genres'].apply(lambda genre: find_films_with_user_query(requested_genres, genre) if requested_genres else True)) &
    #         )]
    #         (filmsTable['isAdult'].apply(lambda isAdult: False if (User.age < 18 and isAdult == 1) else True))
    
    filmsTable = filmsTable[(
            (filmsTable['Writers'].apply(lambda writers: find_films_with_user_query(requested_crew, writers) if requested_crew else True) |
            filmsTable['Directors'].apply(lambda directors: find_films_with_user_query(requested_crew, directors) if requested_crew else True) |
            filmsTable['CrewID'].apply(lambda crew: find_films_with_user_query(requested_crew, crew) if requested_crew else True) |
            filmsTable['Genres'].apply(lambda genre: find_films_with_user_query(requested_genres, genre) if requested_genres else True)) &
            (filmsTable['isAdult'].apply(lambda isAdult: False if (User.age < 18 and isAdult == 1) else True)) |
            (filmsTable['FilmID'] == requested_filmIDs)
            )]
    
    # Store the requested film data
    requested_film = filmsTable[(filmsTable['FilmID'] == requested_filmIDs)]
    if filmsTable.shape[0] > 2000:
        filmsTable = sort_by_highest_imdb_score(filmsTable)[:2000]
        # Check whether we removed the requested film from the table when reducing the size
        if filmsTable[(filmsTable['FilmID'] == requested_filmIDs)].empty:
            filmsTable = pd.concat([filmsTable, requested_film])
    
    filmsTable = filmsTable.reset_index(drop=True)
    requested_film_indices = [int(filmsTable[(filmsTable['FilmID'] == filmID)].index.values) for filmID in original_requested_filmIDs]
    return filmsTable, requested_filmIDs, requested_film_indices

def hybrid_recommender(User):
    """Hybrid Recommender:
    High level function to extract the film query information, create a filmsTable with relevant films,
    call the content recommender and the collaborative recommender and predict the 25 (if possible) most
    similar films, then rank them in order of what it predicts the user will rate the films.
    @param {Person} User
    @returns {Series} Top 25 Film Titles and respective FilmIDs"""
    filmsTable, requested_filmID, requested_film_indices = build_tailored_films_table(User)
   
    collaborative_result = collaborative_recommender()
    content_result = content_recommender(requested_filmID, filmsTable, requested_film_indices)
    film_predictions = []
    for FilmID in content_result['FilmID']:
        film_predictions.append([FilmID, collaborative_result.predict(User.id, FilmID).est])
    film_predictions.sort(key=sort_pred_scores, reverse=True)
    
    #If all films that come back are the same rating (e.g. the results are all the default value)
    maxScore, minScore = calculate_min_max(film_predictions)
    if maxScore == minScore:
        shuffle(film_predictions)

    film_predictions_ids = pd.Series([film[0] for film in film_predictions[:10]])

    suggestedFilms = filmsTable[(filmsTable['FilmID'].isin(film_predictions_ids))]
    return suggestedFilms[['FilmID', 'Title']]#.reset_index(drop=True)

if __name__ == '__main__':
    class Person:
        def __init__(self):
            self.id = 629604219
            self.age = 19
            self.favouriteGenre = 'comedy'
            self.secondFavouriteGenre = 'adventure'
            self.thirdFavouriteGenre = 'action'

    User = Person()
    recommendations = hybrid_recommender(User)
    print(recommendations.iloc[0]['FilmID'])