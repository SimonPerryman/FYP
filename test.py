import os
from nltk.corpus import movie_reviews
os.environ['APPLICATION_PATH'] = r"C:/dev/projects/university/FYP/"
os.environ['PICKLE_DIRECTORY'] = r"C:/dev/projects/university/FYP/pickle_files"
from misc import load_pickle

def test():
    film_reviews = load_pickle('movie_reviews.pkl')
    reviews = [((list(movie_reviews.words(fileid))), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]
    min_len = 1000
    max_len = 0
    for review in reviews:
        len_review = len(review[0])
        if len_review < min_len:
            min_len = len_review
        if len_review > max_len:
            max_len = len_review
    return True

if __name__ == '__main__':
    test()
