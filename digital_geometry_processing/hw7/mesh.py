import numpy  as np


# A = np.array([[1,2],
#               [3,4]])
# b = np.array([1,2])
# print(A.dot(b))

def cross(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return np.array([ay * bz - az * by, -ax * bz + az * bx, ax * by - ay * bx])


def length(a):
    return np.sqrt(sum(a ** 2))


def dot(a, b):
    return a.dot(b)


def normal(a):
    l = length(a)
    if l == 0:
        return np.array([0, 0, 0])
    return a / length(a)


def is_dun(a, b):
    return a.dot(b) < 0

def angle(a, b):
    a = normal(a)
    b = normal(b)
    return np.arccos(a.dot(b))
