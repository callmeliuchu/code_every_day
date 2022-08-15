import numpy as np

mat = np.array([
    [1,2],
    [3,4]
])
u,s,v = np.linalg.svd(mat)
print(u)
print(s)
print(v)
