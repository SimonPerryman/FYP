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
        """Calcuates the document vector for each individual document in the dataset, and then
        combines each individual vector to create a document vector for the dataset. Also stores
        the alphabet for the dataset.
        @param {Boolean} positive - whether to use the positive or negative dataset
        @param {Boolean} binary - whether to calculate the occurence of each word, or presence
                                  of each word in the dataset
        @returns {Numpy Array} dataset_vector"""
        dataset = self.positive_reviews if positive else self.negative_reviews
        cv = CountVectorizer(binary=binary)
        document_vectors = cv.fit_transform(dataset).toarray()
        dataset_vector = np.zeros(document_vectors[0].size, dtype="int")
        for vector in document_vectors:
            dataset_vector = np.add(dataset_vector, vector)
        if not binary:
            if positive:
                self.pos_alphabet = cv.get_feature_names()
                self.pos_alphabet_length = len(self.pos_alphabet)
            else:
                self.neg_alphabet = cv.get_feature_names()
                self.neg_alphabet_length = len(self.neg_alphabet)
        return dataset_vector

    def calculate_TF_vectors(self):
        """Calculates the positive and negative term frequency vectors for the whole dataset"""
        self.pos_tf_vector = self.create_doc_vectors(positive=True, binary=False)
        self.neg_tf_vector = self.create_doc_vectors(positive=False, binary=True)

    def calculate_IDF_vectors(self):
        """Calcuates the positive and negative inverse document frequency vectors for the
        whole dataset"""
        self.pos_idf_vector = self.create_doc_vectors(positive=True, binary=True)
        self.neg_idf_vector = self.create_doc_vectors(positive=False, binary=True)

    def calculate_TF_IDF(self):
        """Calcuates the Term Frequency Inverse Document Frequency values for the whole
        dataset"""
        self.calculate_TF_vectors()
        self.calculate_IDF_vectors()
        self.total_alphabet = list(set(self.pos_alphabet + self.neg_alphabet))
        self.total_alphabet_length = len(self.total_alphabet)
        self.pos_tf_labelled = {}
        self.neg_tf_labelled = {}
        self.pos_idf_labelled = {}
        self.neg_idf_labelled = {}
        self.total_idf_labelled = {}

        # Fills dict with words and their respective tf or idf values
        for index, word in enumerate(self.pos_alphabet):
            self.pos_tf_labelled[word] = self.pos_tf_vector[index]
            self.pos_idf_labelled[word] = self.pos_idf_vector[index]
        for index, word in enumerate(self.neg_alphabet):
            self.neg_tf_labelled[word] = self.neg_tf_vector[index]
            self.neg_idf_labelled[word] = self.neg_idf_vector[index]

        # IDF for both datasets combined
        for word in self.total_alphabet:
            occurs_in_both_datasets = self.pos_idf_labelled.get(word, 0) + self.neg_idf_labelled.get(word, 0)
            self.total_idf_labelled[word] = log10(self.total_alphabet_length / occurs_in_both_datasets)

        self.pos_tf_idf = {}
        self.neg_tf_idf = {}
        self.sum_pos_tf_idf = 0
        self.sum_neg_tf_idf = 0

        # Calculates TF (x in pos or neg) * IDF(x of all documents) and the sum of all those values
        for word in self.pos_tf_labelled:
            self.pos_tf_idf[word] = self.pos_tf_labelled[word] * self.total_idf_labelled[word] #Z
            self.sum_pos_tf_idf += self.pos_tf_idf[word]
        for word in self.neg_tf_labelled:
            self.neg_tf_idf[word] = self.neg_tf_labelled[word] * self.total_idf_labelled[word] #Z
            self.sum_neg_tf_idf += self.neg_tf_idf[word]

    def calculate_probability_values(self):
        """Calcuates the probability of the word appearing in the positive and negative reviews,
        with the addition of the alpha value (default: laplace smoothing)"""
        self.prob_pos = {}
        self.prob_neg = {}
        for word in self.pos_tf_idf:
            self.prob_pos[word] = (self.pos_tf_idf[word] + self.alpha) / (self.sum_pos_tf_idf * (self.alpha * self.pos_alphabet_length))
        for word in self.neg_tf_idf:
            self.prob_neg[word] = (self.neg_tf_idf[word] + self.alpha) / (self.sum_neg_tf_idf * (self.alpha * self.neg_alphabet_length))

    def train(self):
        self.calculate_TF_IDF()
        self.calculate_probability_values()

    def classify(self, review):
        """Calculate the probability a review is positive or negative
        @param {SpaCy Document} Review
        @returns {Boolean} True if review is predicted as negative, False if positive"""
        prob_neg = 0
        prob_pos = 0
        for token in review:
            text = token.text
            if text in self.prob_pos:
                prob_pos += log10(self.prob_pos[text]) - log10(self.sum_pos_tf_idf * (self.alpha * self.pos_alphabet_length))
            if text in self.prob_neg:
                prob_neg += log10(self.prob_neg[text]) - log10(self.sum_neg_tf_idf * (self.alpha * self.neg_alphabet_length))
        return prob_neg >= prob_pos

    def test(self, testingData):
        """Tests the classifier using the testing set.
        @param {List} testingData - list of tuples: (review, category)
        @returns {List} testing_results - list of tuples: (category, prediction)"""
        testing_results = []
        for review, category in testingData:
            prediction = self.classify(review)
            testing_results.append((category, prediction))
        return testing_results
        
def sentiment_analysis():
    # if os.path.isfile('two_reviews_each.pkl'):
        # reviews = load_pickle('two_reviews_each.pkl')
    # else:
    reviews = [(preprocess_reviews(list(movie_reviews.words(fileid))), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)[:10]]
    save_pickle(reviews, 'five_reviews_each.pkl')
    senti = Classifier(reviews)
    senti.train()
        
    return True


if __name__ == "__main__":
    print(sentiment_analysis())