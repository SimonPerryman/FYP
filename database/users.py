import time
import sys
sys.path.insert(0, 'C:/dev/projects/University/FYP/database/')
sys.path.insert(0, 'C:/dev/projects/University/FYP/')

from db_connection import connect
from context import contexts, stages, getStage

def insertUser(UserID, FirstName, LastName):
    try:
        connection = connect()
        currentTime = int(time.time())
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
        #TODO insert logic to set this to be a class
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
            cursor.execute("""UPDATE `users` SET SuggestedFilm = %s WHERE UserID = %s""", (SuggestedFilm, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating user suggested film: ", str(e))
    finally:
        connection.close()