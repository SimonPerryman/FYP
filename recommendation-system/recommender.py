import pandas as pd
from create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_highest_imdb_score():
    return getFilmTable().sort_values('imdb_score', ascending=False)


def generate_cosine_sim(filmsTable=None):
    if filmsTable is None:
        filmsTable = getFilmTable()
    # cv = CountVectorizer(stop_words='english')
    # cv_matrix = cv.fit_transform(filmsTable['metadata'])

    # return cosine_similarity(cv_matrix, cv_matrix)
    hv = HashingVectorizer()
    hv_matrix = hv.fit_transform(filmsTable['metadata'])

    return cosine_similarity(hv_matrix, hv_matrix)

def content_recommendation_system(FilmID, filmsTable=None):
    # # REMOVE # if cosine_similarity is None:


    if filmsTable is None:
        filmsTable = getFilmTable()
    
    filmIndex = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)

    # if filmsTable[(filmsTable['FilmID'] == FilmID)].index.values == 1:
    #     filmIndex = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)
    # else:
    #     filmIndex = None

    #Year RunTime Rating NumberOfVotes imdb_score
    import numpy as np

    filmsTable['Year'] = filmsTable['Year'].astype(np.float16)
    filmsTable['RunTime'] = filmsTable['RunTime'].astype(np.float16) 
    filmsTable['Rating'] = filmsTable['Rating'].astype(np.float16)
    filmsTable['NumberOfVotes'] = filmsTable['NumberOfVotes'].astype(np.int32)
    filmsTable['imdb_score'] = filmsTable['imdb_score'].astype(np.float16)

    cosine_similarity = generate_cosine_sim(filmsTable[:11])

    similarity_scores = list(enumerate(cosine_similarity[filmIndex]))

    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse = True)

    similarity_scores = similarity_scores[1:11]
    print(similarity_scores)

    similar_film_indicies = [index[0] for index in similarity_scores]

    print(filmsTable['Title'].iloc[similar_film_indicies])

    # query = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)
    # print(query)
    # for index in query.index.values:
    #     print(index)
    #     print(type(index))
    # print(query.index.values)
    # print(int(query.index.values))

    # index = filmsTable.set_index('FilmID')
    # print(index.head())
    # # print("long")
    # # print(index[(index['FilmID'] == FilmID)])
    # # print("short")
    # t = index.loc[FilmID]
    # print(t)


    # print("query", query)
    # print(query == "miss jerry")
    # print(query.values)
    # YOU ARE CHECKING THE QUERY INFO


    # print(type(query))
    # print(query == "tt0000009")
    # # print(filmsTable.head())
	


    return True

# content_recommendation_system("tt0000630")

highestFilm = get_highest_imdb_score()

print(highestFilm.iloc[185603])

# indices = pd.Series(filmsTable.index, index=filmsTable['Title']).drop_duplicates()
# print(indices)