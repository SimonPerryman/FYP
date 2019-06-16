"""
Environment Variables File

Adds environment variables on startup.
"""

import os

def add_environment_variables():
    """Adds the environment variables to the system"""
    os.environ['MONGO_DB_NAME'] = "filmio"
    os.environ['CONVERSATION_COLLECTION'] = "conversations"

    os.environ['LOGGING_FORMAT'] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    os.environ['LOGGING_LEVEL'] = "20"

    application_path = os.path.dirname(os.path.realpath(__file__))
    os.environ['APPLICATION_PATH'] = application_path
    os.environ['PICKLE_DIRECTORY'] = "{}/{}".format(application_path, "pickle_files")

    os.environ['BOT_HAPPINESS'] = "3"