import pymysql
import time

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='5q%C270r$xi5cay*c21Gz^5Ss',
                             db='filmio',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def insertUser(UserID, FirstName, LastName, FavouriteGenre = 0,
                SecondFavouriteGenre = 0, ThirdFavouriteGenre = 0):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `users` (UserID, FirstName, LastName,
            Created, FavouriteGenre, SecondFavouriteGenre, ThirdFavouriteGenre) VALUES
            (%s, %s, %s, %s, %s, %s, %s)""", (UserID, FirstName, LastName, int(time.time()),
            FavouriteGenre, SecondFavouriteGenre, ThirdFavouriteGenre))

        connection.commit()
    except Exception as e:
        print("Error inserting user data", str(e))
    finally:
        connection.close()

def updateFavouriteGenres(UserID, FavouriteGenre = 0,
    SecondFavouriteGenre = 0, ThirdFavouriteGenre = 0):
    try:
        with connection.cursor() as cursor:
            if FavouriteGenre != 0:
                cursor.execute("""UPDATE `users` SET FavouriteGenre = %s WHERE UserID = %s""", (FavouriteGenre, UserID))
            if SecondFavouriteGenre != 0:
                cursor.execute("""UPDATE `users` SET SecondFavouriteGenre = %s WHERE UserID = %s""", (SecondFavouriteGenre, UserID))
            if ThirdFavouriteGenre != 0:
                cursor.execute("""UPDATE `users` SET ThirdFavouriteGenre = %s WHERE UserID = %s""", (ThirdFavouriteGenre, UserID))

        connection.commit()
    except Exception as e:
        print("Error updating favourite user genres", str(e))
    finally:
        connection.close()

def getUser(UserID):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM `users` WHERE UserID = %s""", UserID)

        return cursor.fetchone()
    except Exception as e:
        print("Error updating favourite user genres", str(e))
    finally:
        connection.close()