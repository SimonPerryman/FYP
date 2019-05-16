from .db_connection import connect

def getGenre(GenreName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `genreslist` WHERE Name = %s""", (GenreName))
        return cursor.fetchone()
    except Exception as e:
        print("Error getting genre for GenreName: {}".format(GenreName), str(e))
    finally:
        connection.close()


def insertGenre(genre):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO `genreslist` (Name) VALUES (%s)""", (genre))

        connection.commit()
    except Exception as e:
        print("Error inserting genre", str(e))
    finally:
        connection.close()


def getAllAlternativeGenreNamesForGenre(GenreID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM `alternativegenrenames` WHERE Genre_ID = %s", (GenreID))
        return cursor.fetchall()
    except Exception as e:
        print("Error getting all alternative names for genre ID: {}".format(
            GenreID), str(e))
    finally:
        connection.close()

def getAllAlternativeGenreNames():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT AlternativeName, Name, genreslist.GenreID FROM `alternativegenrenames` LEFT JOIN `genreslist`
                                ON genreslist.GenreID = alternativegenrenames.GenreID""")
        return cursor.fetchall()
    except Exception as e:
        print("Error getting all alternative names", str(e))
    finally:
        connection.close()


def insertAlternativeName(GenreName, AlternativeName):
    try:
        GenreID = getGenre(GenreName)['GenreID']
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `alternativegenrenames` (GenreID, AlternativeName)
            VALUES (%s, %s)""", (GenreID, AlternativeName))
        connection.commit()
    except Exception as e:
        print("Error inserting alternative genre name", str(e))
    finally:
        connection.close()


def getGenreByAlternativeGenreName(AlternativeName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `alternativegenrenames` LEFT JOIN `genreslist`
            ON genreslist.GenreID = alternativegenrenames.GenreID
            WHERE AlternativeName = %s""", (AlternativeName))
        result = cursor.fetchone()
        return {"GenreID": result["GenreID"], "Name": result["Name"]}
    except Exception as e:
        print("Error getting genre by alternative genre name", str(e))
    finally:
        connection.close()


def updateFavouriteGenres(UserID, FavouriteGenre=0,
                          SecondFavouriteGenre=0, ThirdFavouriteGenre=0):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            if FavouriteGenre != 0:
                cursor.execute(
                    """UPDATE `favouritegenres` SET GenreID = %s WHERE UserID = %s AND Order = 1""", (FavouriteGenre, UserID))
            if SecondFavouriteGenre != 0:
                cursor.execute(
                    """UPDATE `favouritegenres` SET GenreID = %s WHERE UserID = %s AND Order = 2""", (SecondFavouriteGenre, UserID))
            if ThirdFavouriteGenre != 0:
                cursor.execute(
                    """UPDATE `favouritegenres` SET GenreID = %s WHERE UserID = %s AND Order = 3""", (ThirdFavouriteGenre, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating favourite user genres", str(e))
    finally:
        connection.close()


def getFavouriteGenres(UserID):
    try:
        connection = connect()
        # Check does not already exist
        with connection.cursor() as cursor:
            cursor.execute("""SELECT genreslist.GenreID, Name, favouritegenres.Order FROM favouritegenres
            LEFT JOIN genreslist ON favouritegenres.GenreID = genreslist.GenreID WHERE UserID = %s""", (UserID))

        return cursor.fetchall()
    except Exception as e:
        print("Error getting a user's favourite genres:", str(e))
    finally:
        connection.close()

def getSpecificFavouriteGenre(UserID, Order):
    try:
        if Order > 0 and Order < 4:
            connection = connect()
            # Check does not already exist
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM favouritegenres LEFT JOIN genreslist on 
                favouritegenres.GenreID = genreslist.GenreID WHERE UserID = %s AND `Order` = %s""",
                (UserID, Order))
            
            return cursor.fetchone()
        else:
            return False
    except Exception as e:
        print("Error getting a specific favourite genre for a user:", str(e))
    finally:
        connection.close()


def insertFavouriteGenres(UserID, FavouriteGenre=0,
                          SecondFavouriteGenre=0, ThirdFavouriteGenre=0):
    try:
        connection = connect()
        # Check does not already exist
        with connection.cursor() as cursor:
            if FavouriteGenre != 0:
                cursor.execute(
                    """INSERT INTO `favouritegenres` (`UserID`, `GenreID`, `Order`) VALUES (%s, %s, 1)""", (UserID, FavouriteGenre))
            if SecondFavouriteGenre != 0:
                cursor.execute(
                    """INSERT INTO `favouritegenres` (`UserID`, `GenreID`, `Order`) VALUES (%s, %s, 2)""", (UserID, SecondFavouriteGenre))
            if ThirdFavouriteGenre != 0:
                cursor.execute(
                    """INSERT INTO `favouritegenres` (`UserID`, `GenreID`, `Order`) VALUES (%s, %s, 3)""", (UserID, ThirdFavouriteGenre))

        connection.commit()
    except Exception as e:
        print("Error inserting favourite user genres", str(e))
    finally:
        connection.close()


def getAllGenres():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `genreslist`""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting all genres", str(e))
    finally:
        connection.close()

def getAllFilmGenres():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, GenreID FROM `filmgenrelinked`""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting all film genres", str(e))
    finally:
        connection.close()

def getAllFilmsWithGenreNames():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, Name FROM `filmgenrelinked`
                              LEFT JOIN `genreslist` 
                              ON filmgenrelinked.GenreID = genreslist.GenreID""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting all films with their genre names", str(e))
    finally:
        connection.close()


if __name__ == "__main__":
    print(getFavouriteGenres(629604219))