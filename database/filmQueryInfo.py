from .db_connection import connect

def insertQueryInformation(UserID, Information, Type):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `filmSuggestionQueryInfo` (UserID, Information, Type)
            VALUES (%s, %s, %s)""", (UserID, Information, Type))

        connection.commit()
    except Exception as e:
        print("Error inserting query info:", str(e))
    finally:
        connection.close()

def getQueryInfo(UserID, Type=None):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            if Type:
                cursor.execute("""SELECT Information, Type from `filmSuggestionQueryInfo`
                                    WHERE UserID = %s AND Type = %s""", (UserID, Type))
            else:
                cursor.execute("""SELECT Information, Type from `filmSuggestionQueryInfo`
                                    WHERE UserID = %s""", (UserID))
        return cursor.fetchall()
    except Exception as e:
        print("Error getting film query info", str(e))
    finally:
        connection.close()

def removeQueryInfo(UserID, Type=None):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            if Type:
                cursor.execute("""DELETE FROM `filmSuggestionQueryInfo`
                                WHERE UserID = %s AND Type = %s""", (UserID, Type))
            else:
                cursor.execute("""DELETE FROM `filmSuggestionQueryInfo`
                                WHERE UserID = %s""", (UserID))

        connection.commit()
    except Exception as e:
        print("Error deleting film query info", str(e))
    finally:
        connection.close()
        

if __name__ == "__main__":
    print(getQueryInfo(629604219))
