from .db_connection import connect

def insertReview(UserID, FilmID, Review, Pos, Score):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `reviews` (UserID, FilmID, Review, Pos, Score) VALUES
            (%s, %s, %s, %s, %s)""", (UserID, FilmID, Review, Pos, Score))

        connection.commit()
    except Exception as e:
        print("Error inserting review", str(e))
    finally:
        connection.close()

def getReview(UserID, FilmID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `reviews` WHERE UserID = %s and FilmID = %s""",
                            (UserID, FilmID))
        return cursor.fetchone()
    except Exception as e:
        print("Error inserting review", str(e))
    finally:
        connection.close()