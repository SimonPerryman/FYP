import spacy
nlp = spacy.load('en_core_web_lg')
from database import getAllGenres, getAllAlternativeGenreNames
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/recommendation-system/')
import pandas as pd
import numpy as np

from create_table import getFilmTable
from sklearn.feature_extraction.text import CountVectorizer

def calculate_average_vector(vectors):
  result = np.zeros(vectors.shape[1])
  for vector in vectors:
    result = np.add(result, vector)
  result = result / vectors.shape[0]
  print(result)
  return True

def test():
  message = u'Suggest Wizard of Oz, Avatar a film like the Wizard of Oz and Avatar and Tom Cruise or Peter Simpson'
  message = nlp(message)
  for ent in message.ents:
    if ent.label_ == "WORK_OF_ART":
      print(ent.text)
  # data = [
  #   {"Name": "FirstFilm", "Metadata": "comedy action nm123"},
  #   {"Name": "SecondFilm", "Metadata": "action nm124 nm12"},
  #   {"Name": "ThirdFilm", "Metadata": "thriller action nm123"}
  #   ]
  # df = pd.DataFrame(data, columns=["Name", "Metadata"])
  # print(df.head())
  
  # cv = CountVectorizer(stop_words='english')
  # cv_matrix = cv.fit_transform(df['Metadata'])
  # vectors = cv_matrix.todense()
  # calculate_average_vector(vectors)
  
  
  return True


if __name__ == '__main__':
  test()