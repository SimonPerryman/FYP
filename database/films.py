"""

Films database file

All functions to do with the films and alternative films tables

"""

from .db_connection import connect

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

def getFilmByProcessedName(Name):
    """Searches for a film using its processed named.
    @param {String} Name - Processed Film Name
    @returns {Dict} Result
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, Title FROM `films` WHERE TitlePP = %s""", (Name))

            return cursor.fetchone()
    except Exception as e:
        print("Error getting film id by similar name, with name {}".format(Name), str(e))
    finally:
        connection.close()

def getFilmBySimilarName(Name):
    """Searches for an occurence of a film using its processed named.
    @param {String} Name - Processed Film Name
    @returns {Dict} Result
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, Title FROM `films` WHERE TitlePP LIKE %s""", ('%{}%'.format(Name)))

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