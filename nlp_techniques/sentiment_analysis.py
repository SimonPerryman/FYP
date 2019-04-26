from nltk.corpus import movie_reviews
from random import shuffle
from .preprocessing import preprocess_reviews, preprocess_reviews_keep_stop_words
from sklearn.feature_extraction.text import CountVectorizer
import spacy
import numpy as np
import os
from math import log10
import sys
sys.path.insert(0, os.environ['APPLICATION_PATH'])
from misc import load_pickle, save_pickle
nlp = spacy.load("en_core_web_sm")

# Based on https://github.com/tejank10/Spam-or-Ham/blob/master/spam_ham.ipynb
class Classifier():
    def __init__(self, trainingData):
        self.positive_reviews = [review_information[0] for review_information in trainingData if review_information[1] == 'pos']
        self.negative_reviews = [review_information[0] for review_information in trainingData if review_information[1] == 'neg']
        self.total_reviews = len(self.positive_reviews) + len(self.negative_reviews)
        self.prob_pos_review = len(self.positive_reviews) / self.total_reviews
        self.prob_neg_review = len(self.negative_reviews) / self.total_reviews
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
        # Use ngram range of 2
        cv = CountVectorizer(binary=binary, ngram_range=(1,2))
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
        self.neg_tf_vector = self.create_doc_vectors(positive=False, binary=False)

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
            self.pos_tf_idf[word] = self.pos_tf_labelled[word] * self.total_idf_labelled[word]
            self.sum_pos_tf_idf += self.pos_tf_idf[word]
        for word in self.neg_tf_labelled:
            self.neg_tf_idf[word] = self.neg_tf_labelled[word] * self.total_idf_labelled[word]
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
        @param {String} review
        @returns {Tuple} neg if predicted as negative, pos if predicted as pos and the score"""
        prob_neg = 0
        prob_pos = 0
        for token in nlp(review):
            text = token.text
            if text in self.prob_pos:
                prob_pos += log10(self.prob_pos[text]) - log10(self.sum_pos_tf_idf * (self.alpha * self.pos_alphabet_length)) + log10(self.prob_pos_review)
            if text in self.prob_neg:
                prob_neg += log10(self.prob_neg[text]) - log10(self.sum_neg_tf_idf * (self.alpha * self.neg_alphabet_length)) + log10(self.prob_neg_review)
        score = prob_pos - prob_neg
        return ('neg' if prob_neg >= prob_pos else 'pos', score)

    def test(self, testingData):
        """Tests the classifier using the testing set.
        @param {List} testingData - list of tuples: (review, category)
        @returns {List} testing_results - list of tuples: (category, prediction)"""
        testing_results = []
        for review, category in testingData:
            prediction = self.classify(review)
            testing_results.append((category, prediction))
        return testing_results

def analysis(results):
    correct = 0
    false_positive = 0
    false_negative = 0
    correct_score = 0
    false_pos_score = 0
    false_neg_score = 0
    for result in results:
        if result[0] == result[1][0]:
            correct += 1
            correct_score += result[1][1]
        elif result[0] == 'pos' and result[1][0] == 'neg':
            false_negative += 1
            false_neg_score += result[1][1]
        else:
            false_positive +=1
            false_pos_score += result[1][1]

    print("Correct", correct, "percentage:", correct / 400, "avg score", correct_score / correct)
    print("False Positive", false_positive, "avg false_pos_score", false_pos_score / false_positive)
    print("False negative", false_negative, "avg false_neg_score", false_neg_score / false_negative)

# End of source

def build_film_reviews():
    """Builds the reviews using the nltk movie reviews corpus. Preprocesses the reviews first, then
    saves them as a pickle file before returning them.
    @returns {List} reviews"""
    reviews = [(preprocess_reviews_keep_stop_words(list(movie_reviews.words(fileid))), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]
    save_pickle(reviews, 'movie_reviews.pkl')
    return reviews

def get_film_reviews():
    """Gets the film reviews, building them if they are not saved as a pickle file.
    @returns {List} reviews"""
    if os.path.isfile("{}\{}".format(os.environ['PICKLE_DIRECTORY'], 'movie_reviews.pkl')):
        print("Movie Reviews found, using pickle file.")
        return load_pickle('movie_reviews.pkl')
    else:
        print("Building movie reviews.")
        return build_film_reviews()

def build_classifier():
    """Creates, trains, tests and evaluates the film classifier using the
    nltk movie reviews corpus. The reviews are shuffled in order to randomise
    the results and improve accuracy. Classifier is saved as a pickle file.
    @returns {Classifier} filmClassifier"""
    reviews = get_film_reviews()
    shuffle(reviews)
    trainset = reviews[:1600]
    testset = reviews[1600:]
    filmClassifier = Classifier(trainset)
    filmClassifier.train()
    results = filmClassifier.test(testset)
    analysis(results)
    save_pickle(filmClassifier, "filmClassifier.pkl")
    return filmClassifier

def get_classifier():
    """Gets the film classifier - loading it from memory if
    stored as a pickle file, else creating one if not stored.
    @returns {Classifier} Film Classifier"""
    if os.path.isfile("{}\{}".format(os.environ['PICKLE_DIRECTORY'], 'filmClassifier.pkl')):
        print("Classifier found, using pickle file")
        return load_pickle('filmClassifier.pkl')
    else:
        print("Classifier not found, creating classifier")
        return build_classifier()

def perform_sentiment_analysis(review):
    """Performs sentiment analysis on a user's review,
    classifying it as a positive or negative review"""
    filmClassifier = get_classifier()
    return filmClassifier.classify(preprocess_reviews_keep_stop_words(review))

if __name__ == "__main__":
    print(perform_sentiment_analysis("review"))