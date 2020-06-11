from torchvision import datasets, transforms
from PIL import Image
import pickle
from torchvision import models
import torch.nn as nn
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import io


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


def extract(extracter, img):
    extracter.eval()
    normal_img = load_to_predict(img)
    normal_img.unsqueeze_(dim=0)
    output = extracter(normal_img)
    return output


def img_to_vec(img):
    image_bytes = img.read()
    image = Image.open(io.BytesIO(image_bytes))
    features = extract(extracter, image).data
    features = features.view(2048)
    return features


def get_distance(vector_1, vector_2):
    dot = np.dot(vector_1, vector_2)
    norm_1 = np.linalg.norm(vector_1)
    norm_2 = np.linalg.norm(vector_2)
    cos_dist = dot / (norm_1 * norm_2)
    return cos_dist


class_names = pickle.load(
    open(r'H:\Subject\He co so du lieu da phuong tien\CSDL-DPT20192\DPT\class_names.pkl', 'rb'))
model, extracter = load_model(
    r'H:\Subject\He co so du lieu da phuong tien\CSDL-DPT20192\DPT\dog_classification_resnet.pth', class_names)
