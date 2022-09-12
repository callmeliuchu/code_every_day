import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from digital_geometry_processing.utils import show_obj


def load_obj(path):
    vertices = []
    faces = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('v '):
                arr = line.split(' ')[1:]
                arr = [float(x) for x in arr]
                vertices.append(arr)
            if line.startswith('f '):
                arr = line.split(' ')[1:]
                arr = [int(x) - 1 for x in arr]
                faces.append(arr)
    return np.array(vertices), np.array(faces)


def cross(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return np.array([ay * bz - az * by, -ax * bz + az * bx, ax * by - ay * bx])


def length(a):
    return np.sqrt(sum(a ** 2))


def dot(a, b):
    return a.dot(b)


def uv_load():
    ans = []
    with open('uv', 'r') as f:
        for line in f.readlines():
            arr = line.strip().split(' ')
            a = float(arr[0])
            b = float(arr[-1])
            ans.append([a, b])
    return ans


def mat_load():
    ans = []
    with open('mat', 'r') as f:
        for line in f.readlines():
            arr = line.strip().split(' ')
            ans.append([float(v) for v in arr])
    return ans


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


from collections import defaultdict


class Mesh:

    def __init__(self, path):
        verts, faces = load_obj(path)
        self.vertices = verts
        self.faces = faces
        self.graph = defaultdict(set)
        self.edge2faceid = defaultdict(set)
        self.cots = {}
        for i in range(len(faces)):
            index0 = faces[i][0]
            index1 = faces[i][1]
            index2 = faces[i][2]
            self.graph[index0].add(index1)
            self.graph[index0].add(index2)
            self.graph[index1].add(index0)
            self.graph[index1].add(index2)
            self.graph[index2].add(index1)
            self.graph[index2].add(index0)

            key0 = [index0, index1]
            key1 = [index1, index2]
            key2 = [index2, index0]
            key0.sort()
            key1.sort()
            key2.sort()
            self.edge2faceid[tuple(key0)].add(i)
            self.edge2faceid[tuple(key1)].add(i)
            self.edge2faceid[tuple(key2)].add(i)


def cal(mesh1, mesh2):
    nf = len(mesh1.faces)
    S = [None] * nf
    xx = [None] * nf
    yy = [None] * nf
    area = [0.0] * nf
    angle = [0.0] * nf

    for i in range(nf):
        faces = mesh1.faces
        index0 = faces[i][0]
        index1 = faces[i][1]
        index2 = faces[i][2]
        p0 = mesh1.vertices[index0]
        p1 = mesh1.vertices[index1]
        p2 = mesh1.vertices[index2]
        area[i] = length(cross(p2 - p0, p1 - p0))/ 2.0
        p2_p1 = p2 - p1
        p0_p2 = p0 - p2
        p1_p0 = p1 - p0
        xx[i] = np.array([p2_p1[0], p0_p2[0], p1_p0[0]])
        yy[i] = np.array([-p2_p1[1], -p0_p2[1], -p1_p0[1]])

        _p0 = mesh2.vertices[index0]
        _p1 = mesh2.vertices[index1]
        _p2 = mesh2.vertices[index2]
        u = np.array([_p0[0], _p1[0], _p2[0]])
        v = np.array([_p0[1], _p1[1], _p2[1]])

        J = np.array([
            [yy[i].dot(u) / (2 * area[i]), xx[i].dot(u) / (2 * area[i])],
            [yy[i].dot(v) / (2 * area[i]), xx[i].dot(v) / (2 * area[i])]
        ])
        U, Sigma, VT = np.linalg.svd(J)
        R = U.dot(VT)
        sigama = np.zeros((2, 2))
        sigama[0][0] = Sigma[0]
        sigama[1][1] = Sigma[1]
        S[i] = VT.T.dot(sigama).dot(VT)
        angle[i] = np.arctan2(R[1][0], R[1][1])

    u0 = mesh1.vertices[-1][0]
    v0 = mesh1.vertices[-1][1]
    nv = len(mesh1.vertices)
    A = np.zeros((2 * nv - 2, 2 * nv - 2))
    for i in range(nf):
        face = mesh1.faces[i]
        for m in range(3):
            for n in range(3):
                if face[m] == nv - 1 or face[n] == nv - 1:
                    continue
                else:
                    # print('A1',yy[i][m],xx[i][n],area[i])
                    A[2 * face[m]][2 * face[n]] += yy[i][m] * yy[i][n] / (2 * area[i] * area[i])
                    A[2 * face[m]][2 * face[n]] += xx[i][m] * xx[i][n] / (2 * area[i] * area[i])
                    A[2 * face[m] + 1][2 * face[n] + 1] += yy[i][m] * yy[i][n] / (2 * area[i] * area[i])
                    A[2 * face[m] + 1][2 * face[n] + 1] += xx[i][m] * xx[i][n] / (2 * area[i] * area[i])


    BBB = A
    AAA = csc_matrix(BBB)
    t = 0

    while t < 1.0:
        b = np.zeros((2 * nv - 2, 1))
        for k in range(len(mesh1.faces)):
            theta_t = angle[k] * t
            R = np.array([
                [np.cos(theta_t), -np.sin(theta_t)],
                [np.sin(theta_t), np.cos(theta_t)]
            ])
            A = R.dot((1 - t) * np.identity(2) + t * S[k])
            face = mesh1.faces[k]
            for i in range(3):
                for j in range(3):
                    if face[i] == nv - 1 or face[j] == nv - 1:
                        if face[i] != nv - 1 and face[j] == nv - 1:
                            b[2 * face[i]] -= yy[k][i] * yy[k][j] * u0 / (2 * area[k] * area[k])
                            b[2 * face[i]] -= xx[k][i] * xx[k][j] * u0 / (2 * area[k] * area[k])
                            b[2 * face[i] + 1] -= yy[k][i] * yy[k][j] * v0 / (2 * area[k] * area[k])
                            b[2 * face[i] + 1] -= xx[k][i] * xx[k][j] * v0 / (2 * area[k] * area[k])
                if face[i] != nv - 1:
                    b[2 * face[i]] += yy[k][i] * A[0][0] / area[k]
                    b[2 * face[i]] += xx[k][i] * A[0][1] / area[k]
                    b[2 * face[i] + 1] += yy[k][i] * A[1][0] / area[k]
                    b[2 * face[i] + 1] += xx[k][i] * A[1][1] / area[k]
            # print(AAA.shape,b.shape)
        X = spsolve(AAA, b)

        for i in range(len(mesh1.vertices)):
            if i != nv - 1:
                mesh1.vertices[i] = [X[2 * i], X[2 * i + 1], 0]

        with open('result/{}.obj'.format(int(100*t)), 'a+') as f:
            for vec in mesh1.vertices:
                s = 'v ' + ' '.join([str(v) for v in vec])
                f.write(s + '\n')
            for ff in mesh1.faces:
                s = 'f ' + ' '.join([str(int(v)+1) for v in ff])
                f.write(s + '\n')
        print(t)
        t += 0.01


mesh1 = Mesh('0.000000.obj')
mesh2 = Mesh('1.000000.obj')
cal(mesh1, mesh2)
