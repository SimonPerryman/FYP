import pymysql
import os

def connect():
    return pymysql.connect(host = os.environ['SQL_DB_HOST'],
                             user = os.environ['SQL_DB_USER'],
                             password = os.environ['SQL_DB_PASSWORD'],
                             db = os.environ['SQL_DB_DATABASE_NAME'],
                             charset = "utf8mb4",
                             cursorclass = pymysql.cursors.DictCursor)
    # return pymysql.connect(host="localhost",
    #                         user="root",
    #                         password="5q%C270r$xi5cay*c21Gz^5Ss",
    #                         db="filmio",
    #                         charset="utf8mb4",
    #                         cursorclass=pymysql.cursors.DictCursor)
