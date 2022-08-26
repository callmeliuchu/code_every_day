import numpy as np
from scipy.sparse import csc_matrix,spmatrix
from scipy.sparse.linalg import spsolve,inv

row = np.array([0, 2, 2, 0, 1, 2, 0])
col = np.array([0, 0, 1, 2, 2, 2, 0])
data = np.array([1, 2, 3, 4, 5, 6, 5])
sp_A = csc_matrix((data, (row, col)), shape=(3, 3), dtype=float)
print(sp_A.toarray())
print(csc_matrix(sp_A.toarray()))

b = np.array([[4, 5, 6],[4, 5, 6]]).T
x = spsolve(sp_A, b)
print(type(x))
