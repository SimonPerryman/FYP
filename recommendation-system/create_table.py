"""

If no pandas table exists, create one.

"""

import pandas as pd
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/database/') #TODO Make this an environment variable
import os.path

import films
import genres
import crew
import ratings

def check_film_table_exists():
    if os.path.isfile('filmsTable.pickle'):
        return True
    return False

def remove_duplicate_crew_members(film):
    new_crew = [crew_member for crew_member in film['CrewID'] if crew_member not in film['Directors']]
    new_crew = [crew_member for crew_member in new_crew if crew_member not in film['Writers']]
    return new_crew

# CANT DO YEAR UNLESS change to genre name
def create_metadata(film):
    genres = ' '.join(str(genreID) for genreID in film['GenreID'])
    writers = ' '.join(film['Writers'])
    directors = ' '.join(film['Directors'])
    crew_members = ' '.join(film['CrewID'])
    return '{} {} {} {}'.format(genres, writers, directors, crew_members)

# Change to three functions - get/create/check if already made
def getFilmTable():

    # If table exists return table
    if check_film_table_exists():
        return pd.read_pickle('filmsTable.pickle')
    print('Table not found, creating new table.')
    filmsTable = pd.DataFrame(films.getAllFilms(), columns=['FilmID', 'Title', 'isAdult', 'Year', 'RunTime'])

    filmgenres = pd.DataFrame(genres.getAllFilmGenres(), columns=['FilmID', 'GenreID'])
    filmgenres = filmgenres.groupby('FilmID').agg(lambda x: x.tolist())
    filmsTable = filmsTable.merge(filmgenres, on='FilmID')

    alternativefilmdata = pd.DataFrame(films.getAllNonOriginalAlternativeFilmTitles(), columns=['FilmID', 'AlternativeTitle', 'Region'])
    alternativefilmdata = alternativefilmdata.groupby('FilmID').agg(lambda x: x.tolist())
    filmsTable = filmsTable.merge(alternativefilmdata, on='FilmID')

    WritersAndDirectors = crew.getWritersAndDirectors()
    Writers = []
    Directors = []
    for crew_member in WritersAndDirectors:
        if crew_member['Director'] == 1:
            crew_member.pop('Director', None)
            Directors.append(crew_member)
        else:
            crew_member.pop('Director', None)
            Writers.append(crew_member)
    
    Writers = pd.DataFrame(Writers, columns=['FilmID', 'CrewID'])
    Writers = Writers.groupby('FilmID').agg(lambda x: x.tolist())

    Directors = pd.DataFrame(Directors, columns=['FilmID', 'CrewID'])
    Directors = Directors.groupby('FilmID').agg(lambda x: x.tolist())

    WritersAndDirectors = Writers.merge(Directors, on='FilmID')
    WritersAndDirectors = WritersAndDirectors.rename(index=str, columns={"CrewID_x": "Writers", "CrewID_y": "Directors"})
    filmsTable = filmsTable.merge(WritersAndDirectors, on='FilmID')

    KnownForTitles = pd.DataFrame(crew.getKnownForTitlesTable(), columns=['CrewID', 'KnownForTitle'])
    KnownForTitles = KnownForTitles.rename(index=str, columns={"KnownForTitle": "FilmID"})
    KnownForTitles = KnownForTitles.groupby('FilmID').agg(lambda x: x.tolist())
    filmsTable = filmsTable.merge(KnownForTitles, on='FilmID')

    # Remove duplicate crew members that are also directors/writers.
    filmsTable['CrewID'] = filmsTable.apply(remove_duplicate_crew_members, axis=1)
    
    ratingsTable = pd.DataFrame(ratings.getAllFilmRatings(), columns=['FilmID', 'Rating', 'NumberOfVotes'])
    ratingsTable[['Rating', 'NumberOfVotes']] = ratingsTable[['Rating', 'NumberOfVotes']].apply(pd.to_numeric)

    # WR = (v / (v + m)) * R + (m / (v + m)) * C
    C = ratingsTable['Rating'].mean()
    m = 25000
    ratingsTable['imdb_score'] = ratingsTable.apply(lambda x: (
        x['NumberOfVotes'] / (x['NumberOfVotes'] + m) * x['Rating']) + (m / (m+x['NumberOfVotes']) * C
    ), axis=1)
    
    filmsTable = filmsTable.merge(ratingsTable, on='FilmID')

    filmsTable['metadata'] = filmsTable.apply(create_metadata, axis=1)
    
    print("Saving filmsTable as pickle file")
    filmsTable.to_pickle('filmsTable.pickle')
    return filmsTable

def create_user_film_table():
    """
    Creating the user -> film table matrix
    """
    return True
