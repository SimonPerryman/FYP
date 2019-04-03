from db_connection import connect

def getFilmByID(FilmID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `films` WHERE FilmID = %s""", (FilmID))

        return cursor.fetchone()
    except Exception as e:
        print("Error updating getting Film with FilmID: {} with Error: ".format(FilmID), str(e))
    finally:
        connection.close()

def getFilmBySimilarName(Name):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, Title from `films` WHERE Title LIKE %s""", (Name))

            return cursor.fetchone()
    except Exception as e:
        print("Error getting film id by similar name, with name {}".format(Name), str(e))
    finally:
        connection.close()

def getAllFilms():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `films`""")
        
        return cursor.fetchall()
    except Exception as e:
        print("Error getting all Film Info", str(e))
    finally:
        connection.close()

def getAllNonOriginalAlternativeFilmTitles():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, AlternativeTitle, Region FROM `alternativefilmnames`
                            WHERE Types != 'original' OR Types IS NULL""")
        
        return cursor.fetchall()
    except Exception as e:
        print("Error getting all Film Info", str(e))
    finally:
        connection.close()