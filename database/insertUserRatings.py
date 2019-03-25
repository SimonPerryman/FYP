from db_connection import connect

def insertMultipleUserRatings(ratings):
  try:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.executemany("""INSERT INTO `userRatings`
                            (UserID, FilmID, Liked, Rating)
                            VALUES (%s, %s, %s, %s)""", ratings)

    connection.commit()
  except Exception as e:
    print("Error inserting user data", str(e))
  finally:
    connection.close()

def userRatings(UserID):
  try:
    connection = connect()
    with connection.cursor() as cursor:
      cursor.execute("""SELECT * FROM `userRatings` WHERE UserID = %s""", UserID)

      return cursor.fetchall()
  except Exception as e:
    print("Error fetching user ratings for {}".format(UserID), str(e))
  finally:
    connection.close()

# ratings = [
#   ["629604219", "tt0468569", 1, 4],
#   ["629604219", "tt0372784", 1, 3],
#   ["629604219", "tt4633694", 1, 5],
#   ["629604219", "tt2250912", 1, 4],
#   ["629604219", "tt4154756", 1, 4],
#   ["629604219", "tt0111161", 1, 5],
#   ["629604219", "tt0451079", 0, 1],
#   ["629604219", "tt1013743", 0, 2],
#   ["629604219", "tt0443453", 1, 3],
#   ["629604219", "tt3513498", 1, 3],
#   ["629604219", "tt1131729", 1, 2],
# ]


# insertMultipleUserRatings(ratings)