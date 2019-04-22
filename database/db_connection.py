import pymysql
import os

def connect():
    """Checks to see if it is in the hosted environment, and if so connects
    to the hosted DB, else use the local DB"""
    if 'RDS_HOSTNAME' in os.environ:
        return pymysql.connect(host = os.environ['RDS_HOSTNAME'],
                             user = os.environ['RDS_USERNAME'],
                             password = os.environ['RDS_PASSWORD'],
                             db = os.environ['DB_NAME'],
                             charset = "utf8",
                             cursorclass = pymysql.cursors.DictCursor)
    return pymysql.connect(host="localhost",
                            user="root",
                            password="5q%C270r$xi5cay*c21Gz^5Ss",
                            db="filmio",
                            charset="utf8",
                            cursorclass=pymysql.cursors.DictCursor)
