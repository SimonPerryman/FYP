from configparser import ConfigParser
import logging

config = ConfigParser()

config["settings"] = {
    "logging_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "logging_level": logging.INFO
}

config["SQL_db"] = {
    "host": "localhost",
    "user": "root",
    "password": "5q%C270r$xi5cay*c21Gz^5Ss",
    "db_name": "filmio",
    "charset": "utf8mb4",
}

config["Mongo_db"] = {
    "db_name": "filmio",
    "conversations_collection": "conversations"
}

config["Mongo_db"] = {

}

config["bot"] = {
    "token": r"763546774:AAFEaTaQ5i1CdFQhGgJPiP5EwYrD8TNZCDY"
}

def main():
    with open("config.ini", "w") as f:
        config.write(f)

if __name__ == "__main__":
    main()