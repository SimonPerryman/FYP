import os

def add_environment_variables():
    os.environ['SQL_DB_HOST'] = "localhost"
    os.environ['SQL_DB_USER'] = "root"
    os.environ['SQL_DB_PASSWORD'] = "5q%C270r$xi5cay*c21Gz^5Ss"
    os.environ['SQL_DB_DATABASE_NAME'] = "filmio"

    os.environ['MONGO_DB_NAME'] = "filmio"
    os.environ['CONVERSATION_COLLECTION'] = "conversations"

    os.environ['BOT_TOKEN'] = "763546774:AAFEaTaQ5i1CdFQhGgJPiP5EwYrD8TNZCDY"

    os.environ['LOGGING_FORMAT'] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    os.environ['LOGGING_LEVEL'] = "20"

    os.environ['APPLICATION_PATH'] = "/opt/python/current/app/FilmIO"
