from surprise import SVD
from surprise import KNNBasic
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
import os.path
import pandas as pd
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/')
import database as db
from misc import load_pickle, save_pickle

# Built using "Hands-On Recommendation Systems with Python: Start building powerful and personalized, recommendation engines with Python
# (Rounak Banik 2018)" as base frame

def calc_algo_mean_score(scores):
    """Calcuates the algorithm's mean score
    @param {List} scores
    @returns {Int} algorithm mean score"""
    algo_total_score = 0
    for score in scores:
        algo_total_score += score
    return algo_total_score / len(scores)

def choose_algorithm(dataset):
    """Chooses the best algorithm based on the cross validation scores (SVD vs KNN)
    @param {List} dataset
    @returns {Algorithm Object} Algorithm with highest mean score"""
    svd = cross_validate(SVD(), dataset, measures=['RMSE'], cv=5, verbose=True)
    knn = cross_validate(KNNBasic(), dataset, measures=['RMSE'], cv=5, verbose=True)
    if calc_algo_mean_score(svd['test_rmse']) > calc_algo_mean_score(knn['test_rmse']):
        return SVD()
    return KNNBasic()

def build_collaborative_recommender():
    """Creates the collaborative recommender. Gets all user (of the chatbot) film ratings and the
    stock movie lens film ratings, combines them and makes a dataframe. Using the dataframe, the chosen algorithm
    will be tested and used to predict film ratings for users. The trained algorithm object is saved as a pickle file.
    @returns {Algorithm Object} algorithm"""
    userFilmRatings = db.getAllUserRatings()
    MLFilmRatings = db.getAllMlUserRatings()
    userFilmRatings.extend(MLFilmRatings)
    userFilmRatings = pd.DataFrame(userFilmRatings, columns=['MLUR_ID', 'UserID', 'FilmID', 'Liked', 'Rating'])
    userFilmRatings = userFilmRatings.drop(columns=['MLUR_ID', 'Liked'])
    reader = Reader(rating_scale=(1,5))
    dataset = Dataset.load_from_df(userFilmRatings, reader)
    trainset = dataset.build_full_trainset()
    testset = trainset.build_anti_testset()
    algorithm = choose_algorithm(dataset)    
    algorithm.fit(trainset)
    algorithm.test(testset)

    save_pickle(algorithm, 'collaborative.pkl')
    return algorithm

def get_collaborative_recommender():
    """Loads the algorithm's pickle file from memory
    @returns {Algorithm Object} algorithm"""
    return load_pickle('collaborative.pkl')

def collaborative_recommender():
    """Checks if there is an algorithm object pickle file in memory, if so returns it, else builds a
    collaborative recommendation algorithm object and returns that.
    @returns {Algorithm Object} algorithm"""
    if os.path.isfile('collaborative.pkl'):
        return get_collaborative_recommender()
    else:
        return build_collaborative_recommender()
    
if __name__ == '__main__':
    build_collaborative_recommender()