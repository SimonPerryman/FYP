from .db_connection import connect

def getUserLatestConversationID(UserID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT ConversationID FROM `conversations` WHERE UserID = %s""", UserID)
            results = cursor.fetchall()
            return results[len(results) - 1].get('ConversationID')
    except Exception as e:
        print("Error getting latest conversation ID for a user", str(e))
    finally:
        connection.close()

def insertNewConversation(UserID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `conversations` (UserID) VALUES (%s)""", UserID)
        connection.commit()
    except Exception as e:
        print("Error inserting new conversation", str(e))
    finally:
        connection.close()

def insertMessage(UserID, Message, Timestamp, Intent, Context, Stage, NewConversation):
    try:
        connection = connect()
        if NewConversation == 1:
            insertNewConversation(UserID)
        ConversationID = getUserLatestConversationID(UserID)

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `messages` (ConversationID, Timestamp, Intent, Context, Stage)
            VALUES (%s, %s, %s, %s, %s)""", (ConversationID, Timestamp, Intent, Context, Stage))
            
        connection.commit()
    except Exception as e:
        print("Error inserting message: ", str(e))
    finally:
        connection.close()