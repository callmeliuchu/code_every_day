import numpy as np


mat = np.array([[7,3],[2,9]])
x = np.array([[1,2]]).transpose()

for _ in range(15):
    x = mat.dot(x)
    y = x.T[0]
    print(y[0]/y[1])
    print(y[0]/(y[0]+y[1]),y[1]/(y[0]+y[1]))
