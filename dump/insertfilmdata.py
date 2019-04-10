from db_connection import connect
from crew import getRole
from superhero_films import superhero_titles

namebasics = r'D:\dev\Dataset\name.basics.tsv\data.tsv'
titleakas = r'D:\dev\Dataset\title.akas.tsv\data.tsv'
titlebasics = r'D:\dev\Dataset\title.basics.tsv\data.tsv'
titlecrew = r'D:\dev\Dataset\title.crew.tsv\data.tsv'
titleratings = r'D:\dev\Dataset\title.ratings.tsv\data.tsv'
principals = r'D:\dev\Dataset\title.principals.tsv\data.tsv'

Films = []
FilmIDs = []
Ratings = []
FilmGenreLinked = []
Crew = []
KnownForTitle = []
AlternativeFilmName = []
FilmCrewLinked = []
primaryProfessions = []
Characters = []

def getGenre(genre):
    return {'action': 1, 'adult': 2, 'adventure': 3, 'animation': 5, 'biography': 6, 'comedy': 7, 'crime': 8, 'documentary': 9, 'drama': 10,
             'family': 11, 'fantasy': 12, 'film-noir': 13, 'game-show': 14, 'history': 15, 'horror': 16,
             'music': 17, 'musical': 18, 'mystery': 19, 'news': 20, 'romance': 21, 'sci-fi': 22, 'short': 23, 'sport': 24, 'superhero': 25,
             'talk-show': 26, 'thriller': 27, 'war': 28, 'western': 29}.get(genre, None)

# def insertManyTest(args):
#     try:
#         connection = connect()
#         with connection.cursor() as cursor:
#             test = cursor.executemany("""
#             INSERT INTO `films` (FilmID, Title, isAdult, Year, RunTime) VALUES (%s, %s, %s, %s, %s)
#             """, args)
#         connection.commit()
#     except Exception as e:
#         print("Error execute many", str(e))
#     finally:
#         print("res", test)
#         print("done")
#         connection.close()

# insertManyTest([("34", "12", 1, 1342, 32), ("32", "13", 0, 1232, 43)])

def insertFilmDB(Films):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `films` (FilmID, Title, isAdult,
            Year, RunTime) VALUES (%s, %s, %s, %s, %s)""", Films)

        connection.commit()
    except Exception as e:
        print("Error inserting filmDB data for film: {}, with error:".format(Films[0]), str(e))
    finally:
        connection.close()

def insertFilmGenreLinkedDB(FilmGenre):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `filmgenrelinked` (FilmID, GenreID)
            VALUES (%s, %s)""", FilmGenre)

        connection.commit()
    except Exception as e:
        print("Error inserting filmGenreLinkedDB data for film: {}, with error:".format(FilmGenre[0]), str(e))
    finally:
        connection.close()

def insertAlternativeFilmNameDB(AlternativeFilmName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.executemany("""INSERT INTO `alternativefilmnames` (FilmID, AlternativeTitle, Attributes, Types, Language, Region)
            VALUES (%s, %s, %s, %s, %s, %s)""", AlternativeFilmName)

        connection.commit()
    except Exception as e:
        print("Error inserting AlternativeFilmNameDB data for film: {1}, and title: {2} with error:".format(AlternativeFilmName[0], AlternativeFilmName[1]), str(e))
    finally:
        connection.close()

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

def insertCrewDB(CrewID, Name, birthYear, deathYear):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `crew` (CrewID, Name, birthYear, deathYear)
            VALUES (%s, %s, %s, %s)""", (CrewID, Name, birthYear, deathYear))

        connection.commit()
    except Exception as e:
        print("Error inserting crewDB data for crew: {}, with error:".format(CrewID), str(e))
    finally:
        connection.close()

def insertPrimaryProfessionDB(CrewID, RoleID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `primaryProfessions` (CrewID, RoleID)
            VALUES (%s, %s)""", (CrewID, RoleID))

        connection.commit()
    except Exception as e:
        print("Error inserting primaryProfessionsDB data for crew: {1}, and RoleID: {2}, with error:".format(CrewID, RoleID), str(e))
    finally:
        connection.close()

def insertKnownForTitlesDB(CrewID, KnownForTitle):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `KnownForTitles` (CrewID, KnownForTitle)
            VALUES (%s, %s)""", (CrewID, KnownForTitle))

        connection.commit()
    except Exception as e:
        print("Error inserting KnownForTitlesDB data for crew: {1} with title: {2}, with error:".format(CrewID, KnownForTitle), str(e))
    finally:
        connection.close()

def insertFilmCrewLinkedDB(FilmID, CrewID, RoleID, Job):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `FilmCrewLinked` (FilmID, CrewID, RoleID, Job)
            VALUES (%s, %s, %s, %s)""", (FilmID, CrewID, RoleID, Job))

        connection.commit()
    except Exception as e:
        print("Error inserting FilmCrewLinkedDB data for film: {1} and crew: {2}, and role: {3} with error:".format(FilmID, CrewID, RoleID), str(e))
    finally:
        connection.close()

def insertCharactersDB(FilmID, CrewID, CharacterName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO `characters` (FilmID, CrewID, CharacterName)
            VALUES (%s, %s, %s)""", (FilmID, CrewID, CharacterName))

        connection.commit()
    except Exception as e:
        print("Error inserting CharactersDB data for film: {1} and crew: {2}, and character: {3} with error:".format(FilmID, CrewID, CharacterName), str(e))
    finally:
        connection.close()

def main():
    """Films: Title, isAdult, Year, RunTime,

    AlternativeFilmName: FilmID, Attributes, Types, Language, Region

    Ratings: Film ID, Rating, NumberofVotes

    FILM GENRE LINK: Film ID, GenreID

    Crew: CrewID, Name, birthYear, deathYear

    FILMS&CREW LINK: F&CID, FilmID, CrewID, RoleID, Job

    KnownForTitle: CrewID, KnownForTitle

    PrimaryProfessionsTable: CrewID, RoleID

    CharactersTable: FilmID, CrewID, CharacterName"""

    print("Building Arrays")
    # Build Arrays
    print("Opening titlebasics")
    with open(titlebasics, "r", encoding="utf8") as f1:
        for line in f1:
            formatted = line.strip().lower().split('\t')
            if formatted[1] == "movie":
                # if formatted[7] != "\\n":
                #     formatted[7] = int(formatted[7])
                # else:
                #     formatted[7] = None
                # if formatted[5] != "\\n":
                #     formatted[5] = int(formatted[5])
                # else:
                #     formatted[5] = None
                                # Film ID
                # formatted.append(re.sub(r"[^\s^\d^\w]", "", formatted[2]).replace(" ", ""))
                FilmIDs.append(formatted[0])
                #             # Film ID       #Title          #TitlePP        #isAdult    #Year           #runTime
                # Films.append((formatted[0], formatted[2], formatted[9], int(formatted[4]), formatted[5], formatted[7]))
                # genres = formatted[8].split(",")
                # for genre in genres:
                #     if genre != "\\n":
                #         genreID = getGenre(genre)
                #         if genreID is not None:
                #                                 # FilmID        GenreID
                #                 FilmGenreLinked.append((formatted[0], genreID))
                # if formatted[2] in superhero_titles:
                #     # Add Superhero genre   FilmID      GenreID (For superhero)
                #     FilmGenreLinked.append((formatted[0], 24))
    
    print("opening titleakas")
    x = 0
    with open(titleakas, "r", encoding="utf8") as f2:
        for line in f2:
            formatted = line.strip().lower().split('\t')
            if formatted[0] in FilmIDs and formatted[7] != "1":
                x += 1
                if (x % 10000 == 0 and x != 0) or x == 1:
                    print("Built {} Groups".format(x))
                formatted = line.strip().split('\t')
                                            # FilmID        Title        Attributes      Types       Language        Region
                AlternativeFilmName.append((formatted[0], formatted[2], formatted[6], formatted[5], formatted[4], formatted[3]))

    try:
        with open("dump1.txt", "a", encoding="utf8") as d1:
            d1.write(str(AlternativeFilmName))
    except Exception as e:
        print("Error dumping data", str(e))
    # print("opening titleratings")
    # with open(titleratings, "r", encoding="utf8") as f3:
    #     for line in f3:
    #         formatted = line.strip().split('\t')
    #         if formatted[0] in FilmIDs:
    #             # FilmID, averageRating, numVotes
    #             Ratings.append(formatted)

    # print("opening namebasics")
    # i = 0
    # with open(namebasics, "r", encoding="utf8") as f4:
    #     for line in f4:
    #         if i > 0:
    #             formatted = line.strip().split('\t')
    #             if formatted[3] == "\\N":
    #                 formatted[3] = 0
    #             formatted[4] = formatted[4].split(",")
    #             formatted[5] = formatted[5].split(",")
    #                         #CrewID        Name             birthYear   deathYear
    #             Crew.append(formatted[0], formatted[1], formatted[2], formatted[3])
    #             for primaryProfession in formatted[4]:
    #                 roleID = getRole(primaryProfession).get('rolesListID', None)
    #                 if roleID is not None:
    #                                             # crewID         primaryProfession (roleID)
    #                     primaryProfessions.append([formatted[0], roleID])
    #             for KFT in formatted[5]:
    #                                         # Crew ID, KFT
    #                 KnownForTitle.append([formatted[0], KFT])
    #         i += 1

    # print("opening principals")
    # with open(principals, "r", encoding="utf8") as f5:
    #     for line in f5:
    #         formatted = line.strip().split('\t')
    #         if formatted[5] == r"\\N":
    #             formatted[5] = None
    #         else:
    #             formatted[5] = formatted[5].split(",")
    #         if formatted[0] in FilmIDs:
    #             roleID = getRole(formatted[3]).get('rolesListID', None)
    #             if roleID is not None:
    #                                         # FilmID     CrewID         RoleID  Job
    #                 FilmCrewLinked.append([formatted[0], formatted[2], roleID, formatted[4]])
    #             for character in formatted[5]:
    #                                     # Film ID      # Crew ID     Character Name
    #                 Characters.append([formatted[0], formatted[2], character])
    
    print("Inserting Data")
    # Insert Data
    # Films
    # insertFilmDB(Films)
    # print("Inserted Films")

    # FilmGenreLinked
    # insertFilmGenreLinkedDB(FilmGenreLinked)
    # print("Inserted FilmGenreLinked")

    # AlternativeFilmName
    insertAlternativeFilmNameDB(AlternativeFilmName)
    print("Inserted AlternativeFilmName")

    # Ratings
    # insertRatingsDB(Ratings)
    # print("Inserted Ratings")

    # # Crew
    # for crewMembers in Crew:
    #     insertCrewDB(crewMembers[0], crewMembers[1], crewMembers[2], crewMembers[4])
    # print("Inserted Crew")

    # # primaryProfessions
    # for primaryProfession in primaryProfessions:
    #     insertPrimaryProfessionDB(primaryProfession[0], primaryProfession[1])
    # print("Inserted primaryProfessions")

    # # KnownForTitle
    # for title in KnownForTitle:
    #     insertKnownForTitlesDB(title[0], title[1])
    # print("Inserted KnownForTitle")

    # # FilmCrewLinked
    # for filmCrew in FilmCrewLinked:
    #     insertFilmCrewLinkedDB(filmCrew[0], filmCrew[1], filmCrew[2], filmCrew[3])
    # print("Inserted FilmCrewLinked")

    # # Characters
    # for character in Characters:
    #     insertCharactersDB(character[0], character[1], character[2])
    # print("Inserted Characters")

    print("~~~~~~~~~~~~~~~~~COMPLETE~~~~~~~~~~~~~~~")


if __name__ == "__main__":
    main()