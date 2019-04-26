from .db_connection import connect
from .crew import getRole
from nlp_techniques import preprocess_string

namebasics = r'D:\dev\Dataset\name.basics.tsv\data.tsv'

def create_crew():
    crew = []
    primaryProfessions = []
    KnownForTitle = []
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
            for primaryProfession in formatted[4]:
                if primaryProfession is not None:
                    try:
                        roleID = getRole(primaryProfession).get('rolesListID', None)
                    except Exception as e:
                        print("Error with {}".format(formatted), str(e))
                    if roleID is not None:
                                                # crewID         primaryProfession (roleID)
                        primaryProfessions.append((formatted[0], roleID))
            for KFT in formatted[5]:
                                        # Crew ID, KFT
                KnownForTitle.append((formatted[0], KFT))
    crew.pop(0)
    return crew, primaryProfessions, KnownForTitle

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

def insertPrimaryProfessionDB(primaryProfessions):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `primaryProfessions` (primaryProfessions)
            VALUES (%s, %s)""", primaryProfessions)

        connection.commit()
    except Exception as e:
        print("Error inserting primaryProfessionsDB data for crew: {1}, and RoleID: {2}, with error:".format(primaryProfessions[0], primaryProfessions[1]), str(e))
    finally:
        connection.close()

def insertKnownForTitlesDB(KnownForTitles):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `KnownForTitles` (CrewID, KnownForTitle)
            VALUES (%s, %s)""", KnownForTitles)

        connection.commit()
    except Exception as e:
        print("Error inserting KnownForTitlesDB data for crew: {1} with title: {2}, with error:".format(KnownForTitles[0], KnownForTitles[1]), str(e))
    finally:
        connection.close()

if __name__ == "__main__":
    crew, primaryProfessions, KnownForTitle = create_crew()
    insertCrewDB(crew)
    insertPrimaryProfessionDB(primaryProfessions)
    insertKnownForTitlesDB(KnownForTitle)