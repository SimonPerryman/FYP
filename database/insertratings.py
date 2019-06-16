"""

Ratings data insertion file

"""

from db_connection import connect

def insertRatingsDB(Ratings):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `ratings` (FilmID, Rating, NumberOfVotes)
            VALUES (%s, %s, %s)""", Ratings)

        connection.commit()
    except Exception as e:
        print("Error inserting ratingsDB data for film: {}, with error:".format(Ratings[0]), str(e))
    finally:
        connection.close()
def create_ratings():
    titleratings = r'D:\dev\Dataset\title.ratings.tsv\data.tsv'
    titlebasics = r'D:\dev\Dataset\title.basics.tsv\data.tsv'

    FilmIDs = []
    Ratings = []
    print("Opening titlebasics")
    with open(titlebasics, "r", encoding="utf8") as f1:
        for line in f1:
            formatted = line.strip().lower().split('\t')
            if formatted[1] == "movie":
                FilmIDs.append(formatted[0])

    print("opening titleratings")
    with open(titleratings, "r", encoding="utf8") as f3:
        for line in f3:
            formatted = line.strip().split('\t')
            if formatted[0] in FilmIDs:
                # FilmID, averageRating, numVotes
                Ratings.append((formatted[0], formatted[1], formatted[2]))
    return Ratings

if __name__ == "__main__":
    insertRatingsDB(create_ratings())
    print("Inserted Ratings")