from django.shortcuts import render
import mysql.connector
from mysql.connector import errorcode
import pymysql
import io
import re
import pickle


class CRUD_Post():
    def __init__(self):
        self.post = []

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    # Add a new post

    def _add_post(self, username, pw, url, dbname, post, img):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("INSERT INTO Post (species, weights, heights, colors, access, area, time, status, img, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )")
                records = [(post.spiece, post.weights, post.heights, post.colors, post.access,
                            post.area, post.time, post.status, img, post.type), ]
                empPicture = self.convertToBinaryData(img)
                result = cursor.executemany(query, records)
                cnx.commit()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if (cnx.is_connected()):
                cursor.close()
                cnx.close()

# Get post by id

    def _get_postByID(self, username, pw, url, dbname, id):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("SELECT * FROM Post WHERE id = %s")
                cursor.execute(query, (id,))
                result = cursor.fetchall()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            return result
            if (cnx.is_connected()):
                cursor.close()
                cnx.close()

    # UPDATE post by id

    # Delete post by id

    def _delete_post(self, username, pw, url, dbname, id):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("DELETE FROM Post WHERE id = %s")
                cursor.execute(query, (id,))
                cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if (cnx.is_connected()):
                cursor.close()
                cnx.close()


# db to df

    def db_to_df(self, username, pw, url, dbname):
        try:
            cnx = pymysql.connect(user=username, password=pw,
                                  host=url, database=dbname)
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

# Get dog by dog_type

    def _getDogByType(self, username, pw, url, dbname, type):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("SELECT * FROM dog_type WHERE type = %s")
                cursor.execute(query, (type,))
                result = cursor.fetchall()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if (cnx.is_connected()):
                cursor.close()
                cnx.close()
            return result
