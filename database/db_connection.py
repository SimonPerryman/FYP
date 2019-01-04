from configparser import ConfigParser
import pymysql

config = ConfigParser()
config.read("../config/config.ini")

def connect():
    return pymysql.connect(host=config.get("SQL_db", "host"),
                             user=config.get("SQL_db", "user"),
                             password="5q%C270r$xi5cay*c21Gz^5Ss",
                             db=config.get("SQL_db", "db_name"),
                             charset=config.get("SQL_db", "charset"),
                             cursorclass=pymysql.cursors.DictCursor)
