from db_connection import connect

def getFilmRating(FilmID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `ratings` WHERE FilmID = %s""", (FilmID))

        return cursor.fetchone()
    except Exception as e:
        print("Error getting Film Rating: ", str(e))
    finally:
        connection.close()

def getAllFilmRatings():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, Rating, NumberOfVotes FROM `ratings`""")

        return cursor.fetchall()
    except Exception as e:
        print("Error getting all film ratings: ", str(e))
    finally:
        connection.close()