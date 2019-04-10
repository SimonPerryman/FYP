from nltk.corpus import movie_reviews
from random import shuffle
from preprocessing import preprocess_reviews

def sentiment_analysis():

    reviews = [(preprocess_reviews(list(movie_reviews.words(fileid))), category)
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]
    shuffle(reviews)
    train_data = reviews[:1600]
    test_data = reviews[1600:]
        
    return True


if __name__ == "__main__":
    print(sentiment_analysis())