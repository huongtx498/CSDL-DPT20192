from .IO import *
import numpy as np
from .pic_eval import *

vicinity = {
    'Hoàng Mai': ['Thanh Trì', 'Hai Bà Trưng', 'Thanh Xuân'],
    'Hai Bà Trưng': ['Đống Đa', 'Thanh Xuân', 'Hoàng Mai', 'Hoàn Kiếm'],
    'Đống Đa': ['Hoàn Kiếm', 'Hai Bà Trưng', 'Thanh Xuân', 'Ba Đình', 'Cầu Giấy'],
    'Ba Đình': ['Hoàn Kiếm', 'Đống Đa', 'Cầu Giấy', 'Tây Hồ'],
    'Bắc Từ Liêm': ['Cầu Giấy', 'Tây Hồ', 'Nam Từ Liêm'],
    'Nam Từ Liêm': ['Cầu Giấy', 'Bắc Từ Liêm', 'Thanh Xuân', 'Hà Đông'],
    'Hà Đông': ['Thanh Xuân', 'Nam Từ Liêm'],
    'Tây Hồ': ['Bắc Từ Liêm', 'Ba Đình', 'Cầu Giấy'],
    'Cầu Giấy': ['Tây Hồ', 'Bắc Từ Liêm', 'Nam Từ Liêm', 'Ba Đình', 'Đống Đa'],
    'Thanh Xuân': ['Nam Từ Liêm', 'Hà Đông', 'Hai Bà Trưng', 'Hoàng Mai', 'Đống Đa']
}

# print('Thanh Trì' in vicinity['Hoàng Mai'])
# get point of similar between post and search's post
# form post: list:  (id, species,  wei, hei, colo, accessory, area,         time,                    , status)
#                   (2, 'Komondor', 35, 50, 'Đen', 'Không', 'Thanh Xuân', datetime.date(2020, 5, 20), 'Khỏe mạnh')


def get_point(post, search_post):
    point = 0

    # check weights
    if abs(post[2] - search_post[2]) <= 5:
        point += 1
    elif abs(post[2] - search_post[2]) > 5 and abs(post[2] - search_post[2]) <= 10:
        point += 0.5
    # check heights
    if abs(post[3] - search_post[3]) <= 10:
        point += 1
    elif abs(post[3] - search_post[3]) > 10 and abs(post[3] - search_post[3]) <= 20:
        point += 0.5
    # check color
    if post[4] == search_post[4]:
        point += 1
    # check accessories
    if post[5] == search_post[5]:
        point += 1
    # check area
    if post[6] == search_post[6]:
        point += 1
    elif post[6] in vicinity[search_post[6]]:
        point += 0.5
    # check time
    if abs(post[7] - search_post[7]).days < 2:
        point += 1
    elif abs(post[7] - search_post[7]).days < 5:
        point += 0.5
    # check status
    if post[8] == search_post[8]:
        point += 1

    # print(point)
    # check species dog

    if post[1] in search_post[1]:
        point = point
    elif post[1] == 'Không rõ' or search_post[1] == 'Không rõ':
        point = 0.8*point
    else:
        point = 0.2*point
    # print(point)
    similar_per = point/8
    # print(similar_per)

    # check image
    dog_post_1 = io.BytesIO(post[9])
    dog_post_2 = io.BytesIO(search_post[9])

    vector_1 = img_to_vec(dog_post_1).numpy()
    vector_2 = img_to_vec(dog_post_2).numpy()

    distance = get_distance(vector_1, vector_2)
    # print(distance)
    # post + img: 1-1
    post_similar_percent = (similar_per + distance)/2
    return post_similar_percent


def get_list_post(list_post, search_post):
    list_point = {}
    for post in list_post:
        point = get_point(post, search_post)
        list_point[post] = point
    sort_list_point = sorted(
        list_point.items(), key=lambda p: (p[1], p[0]), reverse=True)
    return sort_list_point
