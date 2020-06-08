import os
import random


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


dog_type = "n02085620-Chihuahua"
getImageByName(dog_type)
