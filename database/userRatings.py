"""

User ratings database file

All functions to do with the user ratings and MovieLens user ratings tables

"""

from .db_connection import connect

def insertMultipleUserRatings(ratings):
  try:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO `userratings`
                            (UserID, FilmID, Liked, Rating)
                            VALUES (%s, %s, %s, %s)""", ratings)

    connection.commit()
  except Exception as e:
    print("Error inserting multiple users data", str(e))
  finally:
    connection.close()

def insertUserRating(UserId, FilmID, Liked, Rating):
  try:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO `userratings`
                        (UserID, FilmID, Liked, Rating)
                        VALUES (%s, %s, %s, %s)""",
                        (UserId, FilmID, Liked, Rating))
  except Exception as e:
    print("Error inserting user rating", str(e))
  finally:
      connection.close()

def getUserRatings(UserID):
  try:
    connection = connect()
    with connection.cursor() as cursor:
      cursor.execute("""SELECT * FROM `userratings` WHERE UserID = %s""", UserID)

      return cursor.fetchall()
  except Exception as e:
    print("Error fetching user ratings for {}".format(UserID), str(e))
  finally:
    connection.close()

def getAllUserRatings():
  try:
    connection = connect()
    with connection.cursor() as cursor:
      cursor.execute("""SELECT * FROM `userratings`""")

      return cursor.fetchall()
  except Exception as e:
    print("Error fetching all user ratings for", str(e))
  finally:
    connection.close()

def getAllMlUserRatings():
  try:
    connection = connect()
    with connection.cursor() as cursor:
      cursor.execute("""SELECT * FROM `mluserratings`""")

      return cursor.fetchall()
  except Exception as e:
    print("Error fetching all movie lens user ratings for", str(e))
  finally:
    connection.close()
