import os
import random
import datetime
import mysql.connector
from mysql.connector import errorcode
import pymysql


modelpath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/dog_classification_resnet.pth'
classnamepath = '/home/trinhhuong/Documents/GitProject/GitHubRepository/CSDL-DPT20192/DPT/find_lostdog/tool/class_names.pkl'
user = 'admin'
pw = 'mmx1437cbcd'
url = 'localhost'
db_name = 'muti_media_db'


class Post():
    def __init__(self, spiece, weights, heights, colors, access, area, time, status, type):
        self.spiece = spiece
        self.weights = weights
        self.heights = heights
        self.colors = colors
        self.access = access
        self.area = area
        self.time = time
        self.status = status
        self.type = type


post = Post("Chihuahua", 40, 50, "Vàng", "Không",
            "Hoàng Mai", datetime.date(2020, 5, 6), "Khỏe mạnh", 1)

post1 = {
    'spiece': "Chihuahua",
    'weights': 40,
    'heights': 50,
    'colors': "Vàng",
    'access': "Không",
    'area': "Hoàng Mai",
    'time': datetime.date(2020, 6, 5),
    'status': "Khỏe mạnh",
    'type': 1,
}


def getImageByName(dog_type):
    folder = "media/Images/"+dog_type
    images = []
    img1 = random.choice(os.listdir(folder))
    img1_url = "media/Images/"+dog_type+"/"+img1
    img2 = random.choice(os.listdir(folder))
    img2_url = "media/Images/"+dog_type+"/"+img2
    images.append(img1_url)
    images.append(img2_url)
    print(images)
    # for filename in os.listdir(folder):
    #     img = mpimg.imread(os.path.join(folder, filename))
    #     if img is not None:
    #         images.append(img)
    return images


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    # print(binaryData)
    return binaryData


def _add_post(username, pw, url, dbname, post, img):
    try:
        cnx = mysql.connector.connect(user=username, password=pw,
                                      host=url, database=dbname)
        if cnx.is_connected():
            cursor = cnx.cursor()
            query = "INSERT INTO Post (species, weights, heights, colors, access, area, time, status, img, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            empPicture = convertToBinaryData(img)
            records = (post.spiece, post.weights, post.heights, post.colors, post.access,
                       post.area, post.time, post.status, empPicture, post.type)
            result = cursor.execute(query, records)
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


dog_type = "n02085620-Chihuahua"
imagepath = getImageByName(dog_type)

_add_post(user, pw, url, db_name, post, imagepath[0])

for img in imagepath:
    print(img + "\n")
    convertToBinaryData(img)
