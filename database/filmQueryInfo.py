from db_connection import connect

def insert_query_information(UserID, Information, Type):
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

def get_query_info(UserID, Type=None):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            if Type:
                cursor.execute("""SELECT Information from `filmSuggestionQueryInfo`
                                    WHERE UserID = %s AND Type = %s""", (UserID, Type))
            else:
                cursor.execute("""SELECT Information from `filmSuggestionQueryInfo`
                                    WHERE UserID = %s""", (UserID))
        return cursor.fetchall()
    except Exception as e:
        print("Error getting film query info", str(e))
    finally:
        connection.close()

def remove_query_info(UserID, Type=None):
    try:
        connection = connect()
        with connection.cursor as cursor:
            if Type:
                cursor.execute("""DELETE FROM `filmSuggestionQueryInfo`
                                WHERE UserID = %s and Type = %s""", (UserID, Type))
            else:
                cursor.execute("""DELETE FROM `filmSuggestionQueryInfo`
                                WHERE UserID = %s""", (UserID))
        return cursor.fetchall()
    except Exception as e:
        print("Error deleting film query info", str(e))
    finally:
        connection.close()
        

if __name__ == "__main__":
    print(get_query_info(123))
    print(get_query_info(123, 1))
    print(get_query_info(123, 3))
    print(get_query_info(123, 5))
    