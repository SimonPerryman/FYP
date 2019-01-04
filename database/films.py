from db_connection import connect

def getFilmByID(FilmID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `films` WHERE FilmID = %s""", (FilmID))

        return cursor.fetchone()
    except Exception as e:
        print("Error updating user age: ", str(e))
    finally:
        connection.close()
