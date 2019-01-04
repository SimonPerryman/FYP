from db_connection import connect


roles = ['actor', 'actress', 'animation_department', "archive_footage", "archive_sound", 'art_department', 'art_director', 'assistant', 'assistant_director', 'camera_department', 'casting_department', 'casting_director', 'cinematographer', 'composer', 'costume_department', 'costume_designer', 'director', 'editor', 'editorial_department', 'electrical_department', 'executive', 'legal', 'location_management',
         'make_up_department', 'manager', 'miscellaneous', 'music_department', 'producer', 'production_department', 'production_designer', 'production_manager', 'publicist', 'script_department', "self", 'set_decorator', 'sound_department', 'soundtrack', 'special_effects', 'stunts', 'talent_agent', 'transportation_department', 'visual_effects', 'writer']


def insertRole(RoleName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO `rolesList` (RoleName) VALUES (%s)""", (RoleName))

        connection.commit()
    except Exception as e:
        print("Error updating user age: ", str(e))
    finally:
        connection.close()

def getRole(RoleName):
    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM `rolesList` WHERE RoleName = %s""", (RoleName))

        return cursor.fetchone()
    except Exception as e:
        print("Error updating user age: ", str(e))
    finally:
        connection.close()
