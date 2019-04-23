from .db_connection import connect

#roles = ['actor', 'actress', 'animation_department', "archive_footage", "archive_sound", 'art_department', 'art_director', 'assistant', 'assistant_director', 'camera_department', 'casting_department', 'casting_director', 'cinematographer', 'composer', 'costume_department', 'costume_designer', 'director', 'editor', 'editorial_department', 'electrical_department', 'executive', 'legal', 'location_management',
#         'make_up_department', 'manager', 'miscellaneous', 'music_department', 'producer', 'production_department', 'production_designer', 'production_manager', 'publicist', 'script_department', "self", 'set_decorator', 'sound_department', 'soundtrack', 'special_effects', 'stunts', 'talent_agent', 'transportation_department', 'visual_effects', 'writer']


def insertRole(RoleName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO `roleslist` (RoleName) VALUES (%s)""", (RoleName))

        connection.commit()
    except Exception as e:
        print("Error inserting role: ", str(e))
    finally:
        connection.close()

def getRole(RoleName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `roleslist` WHERE RoleName = %s""", (RoleName))

        return cursor.fetchone()
    except Exception as e:
        print("Error getting role: ", str(e))
    finally:
        connection.close()

def getWritersAndDirectors():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT FilmID, CrewID, Director FROM `filmwritersanddirectors`""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting writers and directors", str(e))
    finally:
        connection.close()

def getCrewByProcessedName(Name):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT CrewID, Name from `crew` WHERE NamePP LIKE %s""", (Name))

            return cursor.fetchone()
    except Exception as e:
        print("Error getting crew id by processed name, with name {}".format(Name), str(e))
    finally:
        connection.close()

def getCrewBySimilarName(Name):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT CrewID, Name from `crew` WHERE Name LIKE %s""", (Name))

            return cursor.fetchone()
    except Exception as e:
        print("Error getting crew id by similar name, with name {}".format(Name), str(e))
    finally:
        connection.close()

def getCrewByID(CrewID):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT CrewID, Name from `crew` WHERE CrewID = %s""", (CrewID))

            return cursor.fetchone()
    except Exception as e:
        print("Error getting crew info by id, with ID {}".format(CrewID), str(e))
    finally:
        connection.close()
        

def getKnownForTitlesTable():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT CrewID, KnownForTitle FROM `knownfortitles`""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting known for titles table", str(e))
    finally:
        connection.close()

def getAllCrewMembersNames():
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute("""SELECT Name FROM `crew`""")

            return cursor.fetchall()
    except Exception as e:
        print("Error getting crew members names", str(e))
    finally:
        connection.close()