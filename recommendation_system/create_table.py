import pandas as pd
import sys
import os
sys.path.insert(0, os.environ['APPLICATION_PATH'])
import database as db

def check_film_table_exists():
    """Checks if the file exists in the system
    @returns {Boolean} True if found, False if not."""
    return os.path.isfile("{}\{}".format(os.environ['PICKLE_DIRECTORY'], 'filmsTable.pkl'))

def sanitise_genres(genres):
    """Returns a list of genres, removing any null (None) values.
    @param {List} genres
    @returns {List} genres"""
    return [genre for genre in genres if genre != None]

def remove_duplicate_crew_members(film):
    """Removes all crew members that are both in the crew information and are a director/actor.
    @param {Pandas DataFrame} film - one row from the pandas dataframe, including information about the film
    @returns {List} new_crew"""
    new_crew = [crew_member for crew_member in film['CrewID'] if crew_member not in film['Directors']]
    new_crew = [crew_member for crew_member in new_crew if crew_member not in film['Writers']]
    return new_crew

def create_metadata(film, dtype):
    """Creates the metadata field, made up of the genre names, writers, directors and crew id's.
    @param {Pandas DataFrame}  film - one row from the pandas dataframe, including information about the film
    @returns {String} metadata"""
    genres = ' '.join(film['Genres'])
    writers_and_directors = ' '.join(list(set(film['Writers'] + film['Directors'])))
    crew_members = ' '.join(film['CrewID'])
    return '{} {} {}'.format(genres, writers_and_directors, crew_members)

def create_film_table():
    """Creates the general film table, collecting then formatting all the relevant data in the database.
    Calculates IMDB score and film metadata. Finally saves the table as a pickle file.
    @returns {Pandas DataFrame} filmsTable"""
    # Create a dataframe with the film information
    filmsTable = pd.DataFrame(db.getAllFilms(), columns=['FilmID', 'Title', 'isAdult', 'Year', 'RunTime'])

    # Create a dataframe with the genre names and corresponding film IDs, then rename the "Name" column to "Genres"
    filmgenres = pd.DataFrame(db.getAllFilmsWithGenreNames(), columns=['FilmID', 'Name'])
    filmgenres = filmgenres.rename(index=str, columns={'Name': 'Genres'})
    
    # Sanitise the table, removing all null values. Then merge the films df and the genres df
    filmgenres = filmgenres.groupby('FilmID').agg(sanitise_genres)
    filmsTable = filmsTable.merge(filmgenres, on='FilmID')
    print("Preprocessed films data")

    # Create a dataframe with the alternative film data, format the data into lists, such that each film only has
    # one row in the table then merge the films df and the alternative film data df
    alternativefilmdata = pd.DataFrame(db.getAllNonOriginalAlternativeFilmTitles(), columns=['FilmID', 'AlternativeTitle', 'Region'])
    alternativefilmdata = alternativefilmdata.groupby('FilmID').agg(lambda x: x.tolist())
    filmsTable = filmsTable.merge(alternativefilmdata, on='FilmID')
    print("Preprocessed alternative films data")

    # Get writers and directors information and split them into their individual catergories.
    WritersAndDirectors = db.getWritersAndDirectors()
    Writers = []
    Directors = []
    for crew_member in WritersAndDirectors:
        if crew_member['Director'] == 1:
            crew_member.pop('Director', None)
            Directors.append(crew_member)
        else:
            crew_member.pop('Director', None)
            Writers.append(crew_member)
    
    # Create a Writers df and a Directors df, formatting data such that each row in the df
    # corresponds to one row in the df.
    Writers = pd.DataFrame(Writers, columns=['FilmID', 'CrewID'])
    Writers = Writers.groupby('FilmID').agg(lambda x: x.tolist())

    Directors = pd.DataFrame(Directors, columns=['FilmID', 'CrewID'])
    Directors = Directors.groupby('FilmID').agg(lambda x: x.tolist())

    # Merge Writers df and Directors df, rename their columns to "Writers" and "Directors", then
    # merge the singular Writers and Directors df with the film df
    WritersAndDirectors = Writers.merge(Directors, on='FilmID')
    WritersAndDirectors = WritersAndDirectors.rename(index=str, columns={"CrewID_x": "Writers", "CrewID_y": "Directors"})
    filmsTable = filmsTable.merge(WritersAndDirectors, on='FilmID')
    print("Preprocessed writers and directors data")

    # Create crew members df, rename knownfortitle to filmid, then format the data such that
    # each row in the df corresponds to one film. Merge crew members df and film df
    KnownForTitles = pd.DataFrame(db.getKnownForTitlesTable(), columns=['CrewID', 'KnownForTitle'])
    KnownForTitles = KnownForTitles.rename(index=str, columns={"KnownForTitle": "FilmID"})
    KnownForTitles = KnownForTitles.groupby('FilmID').agg(lambda x: x.tolist())
    filmsTable = filmsTable.merge(KnownForTitles, on='FilmID')
    print("Preprocessed known for titles/crew data data")

    # Remove duplicate crew members that are also directors/writers.
    filmsTable['CrewID'] = filmsTable.apply(remove_duplicate_crew_members, axis=1)
    print("Removed duplicate crew members that are also directors or writers")
    
    # Create ratings df, convert the data types to floats.
    ratingsTable = pd.DataFrame(db.getAllFilmRatings(), columns=['FilmID', 'Rating', 'NumberOfVotes'])
    ratingsTable[['Rating', 'NumberOfVotes']] = ratingsTable[['Rating', 'NumberOfVotes']].apply(pd.to_numeric)

    # Create the imdb (Weighted Rating) score using the formula ( https://help.imdb.com/article/imdb/track-movies-tv/faq-for-imdb-ratings/G67Y87TFYYP6TWAV )
    # Weighted Rating = (v / (v + m)) * R + (m / (v + m)) * C
    C = ratingsTable['Rating'].mean()
    m = 25000
    ratingsTable['imdb_score'] = ratingsTable.apply(lambda x: (
        x['NumberOfVotes'] / (x['NumberOfVotes'] + m) * x['Rating']) + (m / (m+x['NumberOfVotes']) * C
    ), axis=1)
    
    # Merge the film df and the ratings df
    filmsTable = filmsTable.merge(ratingsTable, on='FilmID')
    print("Preprocessed ratings data")

    # Create a metadata column in the film df
    filmsTable['metadata'] = filmsTable.apply(create_metadata, axis=1)
    print("Created metadata data")

    print("Saving filmsTable as pickle file")
    filmsTable.to_pickle("{}\{}".format(os.environ['PICKLE_DIRECTORY'],'filmsTable.pkl'))
    return filmsTable

def getFilmTable():
    """Check if film table exists, if so, return it, else create and return it
    @returns {Pandas DataFrame} filmsTable"""
    if check_film_table_exists():
        print('Table found, using pickle file')
        return pd.read_pickle('filmsTable.pkl')
    print('Table not found, creating new table.')
    return create_film_table()

if __name__ == "__main__":
    create_film_table()