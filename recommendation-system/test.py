import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
 
 
data = [
    {"ID": 1, "Metadata": "frog cat orange"},
    {"ID": 2, "Metadata": "frog cat"},
    {"ID": 3, "Metadata": "house frog man"},
    {"ID": 4, "Metadata": "bird man house"},
    {"ID": 5, "Metadata": "tasy food man"},
    {"ID": 6, "Metadata": "dog toad"},
    {"ID": 7, "Metadata": "toad dog hello"}
    # {"ID": 1, "Metadata": "The sun is a star"},
    # {"ID": 2, "Metadata": "My love is like a red, red rose"},
    # {"ID": 3, "Metadata": "Mary had a little lamb"}
]
 
def create_df(data):
    return pd.DataFrame(data=data, columns=["ID", "Metadata"])
 
 
def generate_cosine_sim(df):
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(df['Metadata'])
    print(cv_matrix)
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
 
df = create_df(data)
 
print(generate_cosine_sim(df))
print(generate_cosine_hash_sim(df))