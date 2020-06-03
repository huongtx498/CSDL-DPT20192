from django.shortcuts import render
import mysql.connector
from mysql.connector import errorcode
import re
import pickle
from find_lostdog.model.classify.eval import *


class CRUD_Dog():
    def __init__(self, model_path, class_name_path):
        self.types = []
        self.class_names = pickle.load(open(class_name_path, 'rb'))
        self.model, _ = load_model(model_path, self.class_names)

# '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/dog_classification_resnet.pth'
# '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/class_names.pkl'


# GET all dog_type
    def _get_all_type(self, username, pw, url, dbname):

        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            cursor = cnx.cursor()
            query = ("SELECT type FROM dog_type")
            cursor.execute(query)
            types = [line[0] for line in cursor]
            self.types = types

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
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
                data = cursor.fetchall()
                # list_dogs = [row for row in data]
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
            return data

# GET Dog By iddog_type
    def _get_dogByID(self, username, pw, url, dbname, id):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("SELECT type FROM dog_type WHERE iddog_type = %s")
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
            if (cnx.is_connected()):
                cursor.close()
                cnx.close()
            return result

# Add a new dog_type
    def _add_dog(self, username, pw, url, dbname, dog):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = ("INSERT INTO dog_type (iddog_type, type, from, trait, longevity, piece_range, avg_height, avg_weight, fur_color, seller, note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )")
                records = [(dog.id, dog.type, dog.locate, dog.trait, dog.long, dog.piece,
                            dog.height, dog.weight, dog.color, dog.seller, dog.note), ]
                cursor.execute(query, records)
                cnx.commit()
                context = {
                    'result': 'Add new dog-style successfully!',
                }

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
            return context

# Delete dog_type with id
    def _delete_dog(self, username, pw, url, dbname, id):
        try:
            cnx = mysql.connector.connect(user=username, password=pw,
                                          host=url, database=dbname)
            if cnx.is_connected():
                cursor = cnx.cursor()
                query = """Delete from Laptop where id = %s"""
                cursor.execute(query, (id,))
                cnx.commit()
                context = {
                    'result': 'Delete this dog-style successfully!',
                }
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
            return context
