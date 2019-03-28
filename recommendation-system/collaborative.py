from surprise import SVD
from surprise import KNNBasic
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
import os.path
import pandas as pd
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/database/')
import userRatings
from reco_shared import load_pickle, save_pickle

def calc_algo_mean_score(scores):
    algo_total_score = 0
    for score in scores:
        algo_total_score += score
    return algo_total_score / len(scores)

def choose_algorithm(dataset):
    svd = cross_validate(SVD(), dataset, measures=['RMSE'], cv=5, verbose=True)
    knn = cross_validate(KNNBasic(), dataset, measures=['RMSE'], cv=5, verbose=True)
    if calc_algo_mean_score(svd['test_rmse']) > calc_algo_mean_score(knn['test_rmse']):
        return SVD()
    return KNNBasic()

def build_recommender():
    userFilmRatings = userRatings.getAllUserRatings()
    MLFilmRatings = userRatings.getAllMlUserRatings()
    userFilmRatings.extend(MLFilmRatings)
    userFilmRatings = pd.DataFrame(userFilmRatings, columns=['MLUR_ID', 'UserID', 'FilmID', 'Liked', 'Rating'])
    userFilmRatings = userFilmRatings.drop(columns=['MLUR_ID', 'Liked'])
    reader = Reader(rating_scale=(1,5))
    dataset = Dataset.load_from_df(userFilmRatings, reader)
    trainset = dataset.build_full_trainset()
    testset = trainset.build_anti_testset()

    algorithm = choose_algorithm(dataset)    
    algorithm.fit(trainset)
    predictions = algorithm.test(testset)
    save_pickle(predictions, 'collaborative.pkl')
    return predictions

def get_collaborative_recommender():
    return load_pickle('collaborative.pkl')

def collaborative_recommender(userId):
    if os.path.isfile('collaborative.pkl'):
        collaborative = get_collaborative_recommender()
    else:
        collaborative = build_recommender()
    return [predictions for predictions in collaborative if predictions[0] == userId]

if __name__ == "__main__":
    collaborative_recommender(629604219)