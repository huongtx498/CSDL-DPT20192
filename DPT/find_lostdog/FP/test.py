import pandas as pd 
import numpy as np 

a = np.array([[['a', 1], 2],
        [['b', 3], 4]])
# print(a[0][0][0])
b = pd.DataFrame([x[0] for x in a[:, 0]], columns = ['Id'])
b['Species'] = [x[1] for x in a[:, 0]]
print(b)
print('-------')
print(b.loc[[1]['']])
