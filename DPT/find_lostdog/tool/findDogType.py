import mysql.connector
from mysql.connector import errorcode
from torchvision import transforms
import re
import pickle
import torch
from torchvision import models
import torch.nn as nn


def load_model(model_path, class_names):
    num_class = len(class_names)
    model_ft = models.resnet101(pretrained=True)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, num_class)
    model_ft.load_state_dict(torch.load(
        model_path, map_location=torch.device('cpu')))

    modules = list(model_ft.children())[:-1]
    model_extract = nn.Sequential(*modules)
    return model_ft, model_extract


def load_to_predict(img):
    data_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    norma_img = data_transform(img)
    return norma_img


def predict(model, class_names, img):
    model.eval()
    normal_img = load_to_predict(img)
    normal_img.unsqueeze_(dim=0)
    output = model(normal_img)
    _, pred = torch.topk(output, 3, 1)
    pred = pred.data.squeeze().tolist()
    predict_class = [class_names[k] for k in pred]
    return predict_class


class FindDogType():
    def __init__(self, model_path, class_name_path, username, pw, url, dbname):
        self.types = []
        self.class_names = pickle.load(open(
            class_name_path, 'rb'))
        self.model, _ = load_model(
            model_path, self.class_names)
        self._get_all_type(username, pw,
                           url, dbname)

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

    def find_dog_type(self, img_s=None, tag_s=None):
        tag = []
        img = []
        if tag != None:
            tag = self._find_dog_type_from_tag(tag_s)

        if img != None:
            img = self._find_dog_type_from_img(img_s)

        result = set(tag).intersection(set(img))
        return list(result)

    def _find_dog_type_from_img(self, img):
        types = predict(self.model, self.class_names, img)
        return types

    def _compare_str(self, str1, str2):
        score = sum(c1 != c2 for c1, c2 in zip(str1, str2)) + \
            abs(len(str1) - len(str2))

        return score

    def _find_dog_type_from_tag(self, tag):
        tag = re.sub(r'\W+', '', tag).lower()
        scores = []
        for typ in self.types:
            normal_typ = ' '.join(typ.split('-')[1:])
            normal_typ = re.sub(r'\W+', '', normal_typ).lower()
            score = self._compare_str(tag, normal_typ)
            # print(score)
            scores.append((typ, score))
        scores_sorted = sorted(scores, key=lambda x: x[1])[:5]
        # print(scores_sorted)
        return [typ for (typ, score) in scores_sorted]


if __name__ == '__main__':
    modelpath = r'H:\Subject\He co so du lieu da phuong tien\CSDL-DPT20192\DPT\dog_classification_resnet.pth'
    classnamepath = r'H:\Subject\He co so du lieu da phuong tien\CSDL-DPT20192\DPT\class_names.pkl'
    user = 'admin'
    pw = 'mmx1437cbcd'
    url = 'localhost'
    db_name = 'muti_media_db'
    dog_type = FindDogType(modelpath, classnamepath, user, pw, url, db_name)
    # dog_type = FindDogType('', '', '')

    from PIL import Image
    import io
    with open(r"H:\Subject\He co so du lieu da phuong tien\CSDL-DPT20192\DPT\media\images\n02085620-Chihuahua\n02085620_588.jpg", 'rb') as f:
        image_bytes = f.read()
        image = Image.open(io.BytesIO(image_bytes))
        typ_image = dog_type._find_dog_type_from_img(image)
        print(typ_image)
        typ = dog_type._find_dog_type_from_tag('Chiuahua')
        print(typ)

        intersection = dog_type.find_dog_type(None, 'Chiuahua')
        print(intersection)
