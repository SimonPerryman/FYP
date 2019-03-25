import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_distances as cd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import paired_cosine_distances as pcd
import numpy as np
import math
import pickle
import gc
 
 
data = [
    {"ID": 1, "Metadata": "frog cat orange man frog"},
    {"ID": 2, "Metadata": "frog dog orange red zlat"},
    {"ID": 3, "Metadata": "zlat dog orange man zlat"},
    # {"ID": 3, "Metadata": "house frog man"},
    # {"ID": 4, "Metadata": "bird man house"},
    # {"ID": 5, "Metadata": "tasy food man"},
    # {"ID": 6, "Metadata": "dog toad"},
    # {"ID": 7, "Metadata": "toad dog hello"}
    # {"ID": 1, "Metadata": "The sun is a star"},
    # {"ID": 2, "Metadata": "My love is like a red, red rose"},
    # {"ID": 3, "Metadata": "Mary had a little lamb"}
]
 
def create_df(data):
    return pd.DataFrame(data=data, columns=["ID", "Metadata"])
 
 
def generate_cosine_sim(df):
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(df['Metadata'])
    return cosine_similarity(cv_matrix, cv_matrix)
 
def generate_cosine_hash_sim(df):
    hv = HashingVectorizer(stop_words='english')
    hv_matrix = hv.fit_transform(df['Metadata'])
    print(hv_matrix)
    return cosine_similarity(hv_matrix, hv_matrix)
 
def gen_pickle():
    df = create_df(data)
    cs = generate_cosine_sim(df)
    output = open('cs.pkl', 'wb')
    pickle.dump(cs, output)
    output.close()
 
def calc_cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, np.transpose(vector2))
    magnitude_v1 = math.sqrt(np.dot(vector1, np.transpose(vector1)))
    magnitude_v2 = math.sqrt(np.dot(vector2, np.transpose(vector2)))
    return dot_product / (magnitude_v1 * magnitude_v2)


def generate_cosine_sim_table(filmVectors):
    allFilmSimilarities = []
    for i in range(len(filmVectors)):
        filmVectorSimilarities = []
        for j in range(len(filmVectors)):
            if i == j:
                filmVectorSimilarities.append(1)
            elif i > j:
                filmVectorSimilarities.append(allFilmSimilarities[j][i])
            else:
                filmVectorSimilarities.append(calc_cosine_similarity(filmVectors[i], filmVectors[j]))
        allFilmSimilarities.append(filmVectorSimilarities)
    return allFilmSimilarities
    
f1 = open(r'C:\dev\projects\University\FYP\recommendation-system\hv_matrix.pickle', 'rb')

cv_matrix = pickle.load(f1)

f1.close()

# df = create_df(data)
# cv = CountVectorizer(stop_words='english')
# cv_matrix2 = cv.fit_transform(df['Metadata'])
# cv_matrix3 = cv_matrix2.todense()
# cv_matrix = cv_matrix.todense()
# print(type(cv_matrix))
# print("0", cv_matrix[0])
# print("2", cv_matrix2[0])
# print("3", cv_matrix3[0])
# cv_matrix11 = cv_matrix[:9999].todense()

def save_dense_matrix(matrix, iteration):
    output = open('cv_matrix_part_{}.pickle'.format(iteration), 'wb')

    pickle.dump(matrix, output)

    output.close()

def load_dense_matrix(name):
    # for i in max_i:
    pkl_file = open(name, 'rb')
    dense_matrix = pickle.load(pkl_file)
    pkl_file.close()
    return dense_matrix


max_split = (round(cv_matrix.shape[0] / 5000) * 5000) - 5000
max_i = int(max_split / 5000 + 1)

# from time import sleep
def load_matrix():
    matrix = load_dense_matrix('cv_matrix_part_1.pickle')
    for i in range(2, max_i):
        matrix += load_dense_matrix('cv_matrix_part_{}.pickle'.format(i))
        
    return matrix

# matrix = load_matrix()
# print(matrix)
# print(matrix.shape)
# print(type(matrix))
# print(cv_matrix.shape)

from scipy.sparse import hstack
def save_matricies():
    obj = None
    temp = None
    for split in range(0, max_split, 5000):
        print(split)
        if obj is not None:
            temp = obj
        obj = cv_matrix[split:(split+4999)].todense()
        if temp is not None:
            hstack(obj, temp)
        # save_dense_matrix(obj, int(split / 5000) + 1)
        # del obj
        # gc.collect()
    # obj = cv_matrix[max_split:cv_matrix.shape[0]].todense()
    # gc.collect()
    # save_dense_matrix(obj, max_i)

# save_matricies()

a = cv_matrix[:6721].todense()

output = open('cv_matrix_part_X.pickle', 'wb')

pickle.dump(a, output)

output.close()

# b = cv_matrix[6721:13442].todense()

# output = open('cv_matrix_part_Y.pickle', 'wb')

# pickle.dump(b, output)

# output.close()

# save_dense_matrix()
# matrix5000 = cv_matrix[:4999]
# print(matrix5000)
# print("------")
# pickle5000 = load_dense_matrix('cv_matrix_part_1.pickle')
# print(matrix5000)

# print(cv_matrix[:9999].todense())
# print("---")
# print(type(cv_matrix))

# from scipy.sparse.csc import csc_matrix
# m1 = load_dense_matrix('cv_matrix_part_1.pickle')
# m2 = load_dense_matrix('cv_matrix_part_2.pickle')
# print(hstack())
# print(m1)

# def concatenate_csc_matrices_by_columns(matrix1, matrix2):
#     new_data = np.concatenate((matrix1.data, matrix2.data))
#     new_indices = np.concatenate((matrix1.indices, matrix2.indices))
#     new_ind_ptr = matrix2.indptr + len(matrix1.data)
#     new_ind_ptr = new_ind_ptr[1:]
#     new_ind_ptr = np.concatenate((matrix1.indptr, new_ind_ptr))

#     return csc_matrix((new_data, new_indices, new_ind_ptr), shape=(matrix1.shape[1], matrix1.shape[1] + matrix2.shape[1]))

# print(concatenate_csc_matrices_by_columns(load_dense_matrix('cv_matrix_part_1.pickle'), load_dense_matrix('cv_matrix_part_2.pickle')))


# cv_matrix12 = cv_matrix[10000:19999].todense()
# # print(cv_matrix11)
# print("---")
# print(cv_matrix12)
# print(cv_matrix.toarray())
# sim_table = generate_cosine_sim_table(cv_matrix)



# print(generate_cosine_sim_table(cv_matrix))