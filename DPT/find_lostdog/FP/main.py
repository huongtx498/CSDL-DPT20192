from .IO import *
from .algo import *
from .pic_eval import *
import pandas as pd


class FindPost:
    def __init__(self):
        list_post = db_to_df()
        self.posts = [post for post in list_post if post[10] == 0]
        list_search_post = [post for post in list_post if post[10] == 1]
        self.last_search_post = list_search_post[-1]

    def get_all_post(self):
        # get list post similar
        similar_post_list = get_list_post(self.posts, self.last_search_post)
        similar_post_list = np.asarray(similar_post_list)
        # print(similar_post_list[0][0][0])
        outputs = pd.DataFrame(
            [x[0] for x in similar_post_list[:, 0]], columns=['Id'])
        outputs['Species'] = [x[1] for x in similar_post_list[:, 0]]
        outputs['Weight'] = [x[2] for x in similar_post_list[:, 0]]
        outputs['Height'] = [x[3] for x in similar_post_list[:, 0]]
        outputs['Color'] = [x[4] for x in similar_post_list[:, 0]]
        outputs['Accessory'] = [x[5] for x in similar_post_list[:, 0]]
        outputs['Area'] = [x[6] for x in similar_post_list[:, 0]]
        outputs['Time'] = [x[7] for x in similar_post_list[:, 0]]
        outputs['Status'] = [x[8] for x in similar_post_list[:, 0]]
        outputs['Similarity Rate'] = [x for x in similar_post_list[:, 1]]
        print(outputs)
        return outputs


FindPost = FindPost()
FindPost.get_all_post()
