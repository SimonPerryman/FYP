from .db_connection import connect
from nlp_techniques import preprocess_string

namebasics = r'D:\dev\Dataset\name.basics.tsv\data.tsv'

def create_crew():
    crew = []
    with open(namebasics, "r", encoding="utf8") as f4:
        for line in f4:
            formatted = line.strip().split('\t')
            if formatted[2] == "\\N":
                formatted[2] = None
            if formatted[3] == "\\N":
                formatted[3] = None
            formatted[4] = formatted[4].split(",")
            formatted[5] = formatted[5].split(",")
            formatted.append(preprocess_string(formatted[1]))
                        #CrewID        Name          NamePP        birthYear   deathYear
            crew.append((formatted[0], formatted[1], formatted[6], formatted[2], formatted[3]))
    crew.pop(0)
    return crew

def insertCrewDB(Crew):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `crew` (CrewID, Name, NamePP, birthYear, deathYear)
            VALUES (%s, %s, %s, %s, %s)""", Crew)

        connection.commit()
    except Exception as e:
        print("Error inserting crewDB data, with error:", str(e))
    finally:
        connection.close()

if __name__ == "__main__":
    insertCrewDB(create_crew())