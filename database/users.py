"""

Users database file

All functions related to the user table

"""

from time import time

from .db_connection import connect
from .context import contexts, stages, getStage

def insertUser(UserID, FirstName, LastName):
    try:
        connection = connect()
        currentTime = int(time())
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `users` (UserID, FirstName, LastName,
            Created, Context, Stage, LastMessage) VALUES
            (%s, %s, %s, %s, %s, %s, %s)""", (UserID, FirstName, LastName, currentTime,
            contexts['InitialUserRegistration'], stages['registrationStages']['FirstGenre'], currentTime))

        connection.commit()
    except Exception as e:
        print("Error inserting user data", str(e))
    finally:
        connection.close()

def getUser(UserID):
    """
    @Desription: Get User Information
    @Parameter: UserID (Int)
    """
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `users` WHERE UserID = %s""", UserID)

        return cursor.fetchone()
    except Exception as e:
        print("Error getting user info: ", str(e))
    finally:
        connection.close()

def updateUserAge(UserID, Age):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET Age = %s WHERE UserID = %s""", (Age, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user age: ", str(e))
    finally:
        connection.close()

def setUserContextAndStage(UserID, Context, Stage):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET Context = %s, Stage = %s WHERE UserID = %s""",
                            (Context, Stage, UserID))
        
        connection.commit()
    except Exception as e:
        print("Error updating user contextual stage:", str(e))
    finally:
        connection.close()

def setLastMessage(UserID, LastMessage):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET LastMessage = %s WHERE UserID = %s""", (LastMessage, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user last message time: ", str(e))
    finally:
        connection.close()

def updateSuggestedFilm(UserID, SuggestedFilm):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET SuggestedFilm = %s, SuggestedFilmStatus = 0 WHERE UserID = %s""", (SuggestedFilm, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user suggested film: ", str(e))
    finally:
        connection.close()

def updateSuggestedFilmStatus(UserID, Status):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            if Status == 1:
                cursor.execute("""UPDATE `users` SET SuggestedFilmStatus = %s, SuggestedFilmTime = %s, Asked = %s
                            WHERE UserID = %s""", (Status, time(), 0, UserID))
            else:
                cursor.execute("""UPDATE `users` SET SuggestedFilmStatus = %s, Asked = %s WHERE UserID = %s""", (Status, 0, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user suggested film: ", str(e))
    finally:
        connection.close()

def updateSuggestedFilmIndex(UserID, Index):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET SuggestedFilmIndex = %s WHERE UserID = %s""", (Index, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user suggested film: ", str(e))
    finally:
        connection.close()

def getAllUsersWithSuggestedFilms():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `users` WHERE SuggestedFilmStatus = 1""")

        return cursor.fetchall()
    except Exception as e:
        print("Error getting user all users with suggested films", str(e))
    finally:
        connection.close()

def setAskedCounter(Users):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""UPDATE `users` SET Asked = %s WHERE UserID = %s""", (Users))

        connection.commit()
    except Exception as e:
        print("Error updating users asked counter: ", str(e))
    finally:
        connection.close()

def setAskFilmReview(Users):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""UPDATE `users` SET Context = %s, Stage = %s, previousContext = %s,
                                previousStage = %s WHERE UserID = %s""", (Users))

        connection.commit()
    except Exception as e:
        print("Error updating users context to film review: ", str(e))
    finally:
        connection.close()

def removeSuggestedFilm(UserID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE `users` SET SuggestedFilm = %s, SuggestedFilmStatus = %s,
                            SuggestedFilmIndex = %s, SuggestedFilmTime = %s, Asked = %s
                            WHERE UserID = %s""", (None, 0, 0, 0, 0, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating users context to film review: ", str(e))
    finally:
        connection.close()

def getAllUsers():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `users`""")

        return cursor.fetchall()
    except Exception as e:
        print("Error getting user all users", str(e))
    finally:
        connection.close()