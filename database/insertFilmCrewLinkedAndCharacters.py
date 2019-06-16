"""

Film and Crew data insertion file

"""

from .crew import getRole
from .db_connection import connect
principals = r'D:\dev\Dataset\title.principals.tsv\data.tsv'
titlebasics = r'D:\dev\Dataset\title.basics.tsv\data.tsv'

def insertFilmCrewLinkedDB(FilmCrewLinked):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `FilmCrewLinked` (FilmID, CrewID, RoleID, Job)
            VALUES (%s, %s, %s, %s)""", FilmCrewLinked)

        connection.commit()
    except Exception as e:
        print("Error inserting FilmCrewLinkedDB data for film: {1} and crew: {2}, and role: {3} with error:".format(FilmCrewLinked[0], FilmCrewLinked[1], FilmCrewLinked[3]), str(e))
    finally:
        connection.close()

def insertCharactersDB(Characters):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `characters` (FilmID, CrewID, CharacterName)
            VALUES (%s, %s, %s)""", Characters)

        connection.commit()
    except Exception as e:
        print("Error inserting CharactersDB data for film: {1} and crew: {2}, and character: {3} with error:".format(Characters[0], Characters[1], Characters[2]), str(e))
    finally:
        connection.close()

def create_film_ids():
    FilmIDs = []
    print("Opening titlebasics")
    with open(titlebasics, "r", encoding="utf8") as f1:
        for line in f1:
            formatted = line.strip().lower().split('\t')
            if formatted[1] == "movie":
                FilmIDs.append(formatted[0])
    return FilmIDs

def create_data(FilmIDs):
    FilmCrewLinked = []
    Characters = []
    print("opening principals")
    with open(principals, "r", encoding="utf8") as f5:
        for line in f5:
            formatted = line.strip().split('\t')
            if formatted[5] == r"\\N":
                formatted[5] = None
            else:
                formatted[5] = formatted[5].split(",")
            if formatted[0] in FilmIDs:
                roleID = getRole(formatted[3]).get('rolesListID', None)
                if roleID is not None:
                                            # FilmID     CrewID         RoleID  Job
                    FilmCrewLinked.append((formatted[0], formatted[2], roleID, formatted[4]))
                for character in formatted[5]:
                                        # Film ID      # Crew ID     Character Name
                    Characters.append((formatted[0], formatted[2], character))
    return Characters, FilmCrewLinked

if __name__ == "__main__":
    Characters, FilmCrewLinked = create_data(create_film_ids())
    
    # FilmCrewLinked
    insertFilmCrewLinkedDB(FilmCrewLinked)
    print("Inserted FilmCrewLinked")

    # Characters
    insertCharactersDB(Characters)
    print("Inserted Characters")