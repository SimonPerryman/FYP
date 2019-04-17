import os

def add_environment_variables():
    """Adds the environment variables to the system"""
    os.environ['MONGO_DB_NAME'] = "filmio"
    os.environ['CONVERSATION_COLLECTION'] = "conversations"

    os.environ['LOGGING_FORMAT'] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    os.environ['LOGGING_LEVEL'] = "20"

    os.environ['APPLICATION_PATH'] = os.path.dirname(os.path.realpath(__file__))
