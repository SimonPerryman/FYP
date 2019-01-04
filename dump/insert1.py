from crew import getRole
from db_connection import connect

namebasics = r'D:\dev\Dataset\name.basics.tsv\data.tsv'

Crew = []
primaryProfessions = []
KnownForTitle = []

def insertCrewDB(Crew):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `crew` (CrewID, Name, birthYear, deathYear)
            VALUES (%s, %s, %s, %s)""", Crew)

        connection.commit()
    except Exception as e:
        print("Error inserting crewDB data for crew: {}, with error:".format(Crew[0]), str(e))
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

print("opening namebasics")
i = 0
with open(namebasics, "r", encoding="utf8") as f4:
    for line in f4:
        if i > 0:
            formatted = line.strip().split('\t')
            if formatted[3] == "\\N":
                formatted[3] = 0
            formatted[4] = formatted[4].split(",")
            formatted[5] = formatted[5].split(",")
                        #CrewID        Name             birthYear   deathYear
            Crew.append((formatted[0], formatted[1], formatted[2], formatted[3]))
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
        i += 1

# Crew
insertCrewDB(Crew)
print("Inserted Crew")

# primaryProfessions
insertPrimaryProfessionDB(primaryProfessions)
print("Inserted primaryProfessions")

# KnownForTitle
insertKnownForTitlesDB(KnownForTitle)
print("Inserted KnownForTitle")
