from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
import pandas as pd
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/database/')
import userRatings

def collaborative_recommender():
    ml_ratings = pd.DataFrame(userRatings.getAllMlUserRatings(), columns=['MLUR_ID', 'UserID', 'FilmID', 'Liked', 'Rating']).drop('ML_URID')
    print(ml_ratings.head())
    # data100 = Dataset.load_builtin('ml-100k')
    # data1m = Dataset.load_builtin('ml-1m')

    # return True
if __name__ == "__main__":
    collaborative_recommender()