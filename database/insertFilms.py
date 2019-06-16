"""

IMDB films data insertion file

"""

from .db_connection import connect
from nlp_techniques import preprocess_string

def insertFilmDB(Films):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `films` (FilmID, Title, TitlePP, isAdult,
            Year, RunTime) VALUES (%s, %s, %s, %s, %s, %s)""", Films)

        connection.commit()
    except Exception as e:
        print("Error inserting filmDB data for film: {}, with error:".format(Films[0]), str(e))
    finally:
        connection.close()

def construct_films_data():
    titlebasics = r'D:\dev\Dataset\title.basics.tsv\data.tsv'
    Films = []
    with open(titlebasics, "r", encoding="utf8") as f1:
        for line in f1:
            formatted = line.strip().split('\t')
            if formatted[1] == "movie":
                if formatted[7] != "\\N":
                    formatted[7] = int(formatted[7])
                else:
                    formatted[7] = None
                if formatted[5] != "\\N":
                    formatted[5] = int(formatted[5])
                else:
                    formatted[5] = None
                formatted.append(preprocess_string(formatted[2]))
                            # Film ID       #Title          #TitlePP        #isAdult    #Year           #runTime
                Films.append((formatted[0].lower(), formatted[2], formatted[9], int(formatted[4]), formatted[5], formatted[7]))
    return Films
    
if __name__ == "__main__":
    insertFilmDB(construct_films_data())