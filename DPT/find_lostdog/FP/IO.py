import mysql.connector
from mysql.connector import errorcode
import pymysql
import io


def db_to_df():
    try:
        cnx = pymysql.connect(user='admin', password='mmx1437cbcd',
                              host='localhost', database='muti_media_db')
        cursor = cnx.cursor()
        query = ("SELECT * FROM Post")
        cursor.execute(query)
        data = cursor.fetchall()
        list_post = [row for row in data]
        return list_post

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()
