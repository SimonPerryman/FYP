import pandas as pd
from create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

filmsTable = getFilmTable()

def get_highest_imdb_score():
    return getFilmTable().sort_values('imdb_score', ascending=False)


def generate_cosine_sim():
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(getFilmTable()['metadata'])

    return cosine_similarity(cv_matrix, cv_matrix)

def content_recommendation_system(FilmID, filmsTable=None):
    # # REMOVE # if cosine_similarity is None:
    # cosine_similarity = generate_cosine_sim()
    # print(cosine_similarity)

    if filmsTable is None:
        filmsTable = getFilmTable()

    print(filmsTable.head())

    # query = filmsTable[(filmsTable['FilmID'] == FilmID)]

    index = filmsTable.set_index('FilmID')
    print(index.head())
    # print("long")
    # print(index[(index['FilmID'] == FilmID)])
    # print("short")
    t = index.loc[FilmID]
    print(t)


    # print("query", query)
    # print(query == "miss jerry")
    # print(query.values)
    # YOU ARE CHECKING THE QUERY INFO


    # print(type(query))
    # print(query == "tt0000009")
    # # print(filmsTable.head())
	


    return True

content_recommendation_system("tt0000009")

# indices = pd.Series(filmsTable.index, index=filmsTable['Title']).drop_duplicates()
# print(indices)