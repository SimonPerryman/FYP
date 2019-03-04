"""

If no pandas table exists, create one.

"""

import pandas as pd
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/database/') #TODO Make this an environment variable

import films
import genres
import crew
import ratings

Table = False

# Change to three functions - get/create/check if already made
def getFilmTable():

    # If table exists return table
    if Table:
        return Table

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

    ratingsTable = pd.DataFrame(ratings.getAllFilmRatings(), columns=['FilmID', 'Rating', 'NumberOfVotes'])
    ratingsTable[['Rating', 'NumberOfVotes']] = ratingsTable[['Rating', 'NumberOfVotes']].apply(pd.to_numeric)

    # WR = (v / (v + m)) * R + (m / (v + m)) * C
    C = ratingsTable['Rating'].mean()
    m = 25000
    ratingsTable['imdb_score'] = ratingsTable.apply(lambda x: (
        x['NumberOfVotes'] / (x['NumberOfVotes'] + m) * x['Rating']) + (m / (m+x['NumberOfVotes']) * C
    ), axis=1)
    
    filmsTable = filmsTable.merge(ratingsTable, on='FilmID')
 
    return filmsTable

    # query = filmsTable[(filmsTable['FilmID'] == "tt0000147")]

getFilmTable()