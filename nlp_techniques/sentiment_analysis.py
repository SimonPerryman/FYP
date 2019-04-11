from nltk.corpus import movie_reviews
from random import shuffle
from preprocessing import preprocess_reviews
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import spacy
import numpy as np
import os.path
from math import log10
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/')
from misc import load_pickle, save_pickle
nlp = spacy.load("en_core_web_sm")

class Classifier():
    def __init__(self, trainingData):
        self.positive_reviews = [review_information[0] for review_information in trainingData if review_information[1] == 'pos']
        self.negative_reviews = [review_information[0] for review_information in trainingData if review_information[1] == 'neg']
        self.alpha = 1

    def create_doc_vectors(self, positive, binary):
        dataset = self.positive_reviews if positive else self.negative_reviews
        cv = CountVectorizer(binary=binary)
        document_vectors = cv.fit_transform(dataset).toarray()
        dataset_vector = np.zeros(document_vectors[0].size, dtype="int")
        for vector in document_vectors:
            dataset_vector = np.add(dataset_vector, vector)
        dataset_words = {}
        for index, word in enumerate(cv.get_feature_names()):
            dataset_words[word] = dataset_vector[index]
        return dataset_vector, cv.get_feature_names()       

    def calcuate_IDF_matrix(self, positive):
        dataset = self.positive_reviews if positive else self.negative_reviews
        dataset_vector, alphabet = self.create_doc_vectors(positive, True)
        number_of_documents = len(dataset)
        idf_matrix = np.zeros(len(alphabet))
        for index in range(len(alphabet)):
            idf_matrix[index] = log10(dataset_vector[index] / number_of_documents)
        return idf_matrix
    
    def calculate_TF_matrix(self, positive):
        dataset_vector, alphabet = self.create_doc_vectors(positive, False)
        alphabet_length = len(alphabet)
        tf_matrix = np.zeros(len(alphabet))
        for index in range(alphabet_length):
            tf_matrix[index] = dataset_vector[index] / alphabet_length
        return tf_matrix

    def calculate_TF_IDF_matrix(self, positive):
        tf_matrix = self.calculate_TF_matrix(positive)
        idf_matrix = self.calcuate_IDF_matrix(positive)
        sum_of_all_words_tf_idf = np.add.reduce(tf_matrix * idf_matrix, 0)
        vector_size = tf_matrix.size
        tf_idf_matrix = np.zeros(vector_size)
        for index in range(vector_size):

            tf_idf_matrix[index] = ((tf_matrix[index] * idf_matrix[index]) + self.alpha) / (sum_of_all_words_tf_idf + (sum_of_all_words_tf_idf * self.alpha))
        return tf_idf_matrix

    def train(self):
        self.positive_tf_idf_matrix = self.calculate_TF_IDF_matrix(True)
        self.negative_tf_idf_matrix = self.calculate_TF_IDF_matrix(False)

    def classify(self, review):
        print("review")


def sentiment_analysis():
    if os.path.isfile('two_reviews_each.pkl'):
        reviews = load_pickle('two_reviews_each.pkl')
    else:
        reviews = [(preprocess_reviews(list(movie_reviews.words(fileid))), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)[:2]]
        save_pickle(reviews, 'two_reviews_each.pkl')
    senti = Classifier(reviews)
    senti.train()
        
    return True


if __name__ == "__main__":
    print(sentiment_analysis())