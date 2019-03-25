import pandas as pd
import pickle
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

    # output = open('cv_matrix.pickle', 'wb')

    # pickle.dump(cv_matrix, output)

    # output.close()

    # return cosine_similarity(cv_matrix, cv_matrix)
    hv = HashingVectorizer()
    hv_matrix = hv.fit_transform(filmsTable['metadata'])

    output = open('hv_matrix.pickle', 'wb')

    pickle.dump(hv_matrix, output)

    output.close()

    return cosine_similarity(hv_matrix, hv_matrix)

z = set()
def calc(x):
    a = x.split()
    for b in a:
        z.add(b)

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

    # cosine_similarity = generate_cosine_sim(filmsTable)

    ind = filmsTable['metadata'].apply(calc)

    # similarity_scores = list(enumerate(cosine_similarity[filmIndex]))

    # similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse = True)

    # similarity_scores = similarity_scores[1:11]

    # similar_film_indicies = [index[0] for index in similarity_scores]

    # print(filmsTable['Title'].iloc[similar_film_indicies])

    # query = int(filmsTable[(filmsTable['FilmID'] == FilmID)].index.values)
	
    return True

# print(content_recommendation_system("tt0000630"))

f1 = open('cv_matrix.pickle', 'rb')

zg = pickle.load(f1)

f1.close()
print(zg)

# print(cosine_similarity(zg, zg))
# highestFilm = get_highest_imdb_score()

# print(highestFilm.iloc[185603])

# indices = pd.Series(filmsTable.index, index=filmsTable['Title']).drop_duplicates()
# print(indices)
