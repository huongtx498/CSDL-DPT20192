import torch
from torchvision import models
import torch.nn as nn
import matplotlib.pyplot as plt
from .utils import imshow
from .loader import load_to_predict


def visualize_model(model, dataloaders, class_names, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():  # same torch.set_grad_enabled(False)
        for i, (inputs, labels) in enumerate(dataloaders['val']):

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            for j in range(inputs.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images//2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(inputs.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return
        model.train(mode=was_training)


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


def predict(model, class_names, img):
    model.eval()
    normal_img = load_to_predict(img)
    normal_img.unsqueeze_(dim=0)
    output = model(normal_img)
    _, pred = torch.topk(output, 3, 1)
    pred = pred.data.squeeze().tolist()
    predict_class = [class_names[k] for k in pred]
    return predict_class


def extract(extracter, img):
    extracter.eval()
    normal_img = load_to_predict(img)
    normal_img.unsqueeze_(dim=0)
    output = extracter(normal_img)
    return output


if __name__ == '__main__':
    import pickle
    class_names = pickle.load(open('.\\class_names.pkl', 'rb'))

    model, extracter = load_model('dog_classification_resnet.pth', class_names)

    from PIL import Image
    import io
    with open(".\\dataset\\val\\n02085620-Chihuahua\\n02085620_588.jpg", 'rb') as f:
        image_bytes = f.read()
        image = Image.open(io.BytesIO(image_bytes))
        features = extract(extracter, image).data
        features = features.view(2048)
        print(features)
        print(features.shape)
        typ = predict(model, class_names, image)
        print(typ)
