from db_connection import connect
import films
import pandas as pd
import math
from random import random

def sanitise_ratings(rating):
  return math.ceil(rating)

def sanitise_imdb_id(id):
  num_zeros = "0" * (7 - len(id))
  return 'tt{}{}'.format(num_zeros, id)

def calc_like_or_dislike(rating):
  if rating == 5:
    return 1
  elif rating == 4:
    return 1 if random() > 0.2 else 0
  elif rating == 3:
    return 1 if random() > 0.5 else 0
  elif rating == 2:
    return 1 if random() > 0.8 else 0
  else:
    return 0

def construct_movie_lens_ratings():
  ml_to_imdb_ratings = []
  with open(r'D:\dev\Dataset\movie_lens\links.csv', 'r') as f1:
    for line in f1:
      line = line.split(',')
      line[1] = sanitise_imdb_id(line[1])
      ml_to_imdb_ratings.append([line[0], line[1]])
  ml_to_imdb_ratings.pop(0)

  ml_to_imdb_ratings = pd.DataFrame(ml_to_imdb_ratings, columns=['movieId', 'IMDB_ID'])
  ml_to_imdb_ratings['movieId'] = pd.to_numeric(ml_to_imdb_ratings['movieId'])

  ml_ratings = pd.read_csv(r'D:\dev\Dataset\movie_lens\ratings.csv')
  ml_ratings = ml_ratings.drop(columns=['timestamp'])
  ml_ratings['rating'] = ml_ratings['rating'].apply(sanitise_ratings)

  ml_table_complete = pd.merge(ml_ratings, ml_to_imdb_ratings, how='left', on='movieId')
  ml_table_complete = ml_table_complete.rename(index=str, columns={'movieId': 'ML_ID', 'IMDB_ID': 'FilmID'})

  filmsTable = pd.DataFrame(films.getAllFilms(), columns=['FilmID', 'Title', 'isAdult', 'Year', 'RunTime'])
  relevant_ml_films_table = ml_table_complete[(ml_table_complete['FilmID'].isin(filmsTable['FilmID']))]
  relevant_ml_films_table = relevant_ml_films_table.drop(columns=['ML_ID'])
  relevant_ml_films = relevant_ml_films_table.values.tolist()
  for film in relevant_ml_films:
    temp = film[1]
    film[1] = film[2]
    film[2] = calc_like_or_dislike(temp)
    film.append(temp)

  return relevant_ml_films

def insert_movie_lens_ratings(movie_ratings):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `mlUserRatings`
                                (UserID, FilmID, Liked, Rating)
                                VALUES (%s, %s, %s, %s)""", movie_ratings)

        connection.commit()
    except Exception as e:
        print("Error inserting user data", str(e))
    finally:
        connection.close()


if __name__ == "__main__":
  insert_movie_lens_ratings(construct_movie_lens_ratings())