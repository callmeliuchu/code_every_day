import numpy as np
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
import copy


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

        W = np.zeros((len(self.vertices), len(self.vertices)))
        for i, (v0, v1, v2) in enumerate(self.faces):
            W[v0][v1] = 1
            W[v1][v2] = 1
            W[v2][v0] = 1

        fix_handles = []
        with open("fix.txt", "r") as f:
            for line in f.readlines():
                if line.strip():
                    fix_handles.append(int(line.strip()))

        fix_handles = fix_handles[1:]

        m_handles = []
        m_pos_handles = []

        with open("move.txt", "r") as f:
            for line in f.readlines():
                if line.strip():
                    arr = line.split(' ')
                    if len(arr) == 4:
                        m_handles.append(int(arr[0]))
                        m_pos_handles.append([float(v) for v in arr[1:]])

        m_pos_handles = np.array(m_pos_handles)
        handles = m_handles + fix_handles
        fix_handles = np.array(fix_handles)
        handles = np.array(handles)

        laplacian = np.zeros((len(self.vertices), len(self.vertices)))
        for idx in self.graph:
            if idx in handles:
                laplacian[idx][idx] = 1
                continue
            ww = 0
            for u in self.graph[idx]:
                # if idx not in boundary_vids or u not in boundary_vids:
                w = W[idx][u] + W[u][idx]
                ww += w
                laplacian[idx][u] = -w
            laplacian[idx][idx] = ww

        pos_ref = copy.deepcopy(self.vertices)

        b = np.zeros((len(self.vertices), 3))
        for _ in range(10):
            lts = []
            for i in range(len(self.vertices)):
                J = np.zeros((3, 3))
                for j in self.graph[i]:
                    e_ = pos_ref[i] - pos_ref[j]
                    ep_ = self.vertices[i] - self.vertices[j]
                    w = W[i][j] + W[j][i]
                    e = np.array([e_])
                    ep = np.array([ep_]).T
                    J += w * (e*ep)


                U, S, V = np.linalg.svd(J)
                R = U.dot(V)

                if np.linalg.det(R) < 0:
                    U[0][2] *= -1
                    U[1][2] *= -1
                    U[2][2] *= -1
                    R = U.dot(V)
                lts.append(R)

            for i in range(len(self.vertices)):
                b_tmp = np.array([0.0, 0.0, 0.0])

                for j in self.graph[i]:
                    ep = pos_ref[i] - pos_ref[j]
                    JR = lts[i] + lts[j]
                    w = (W[i][j] + W[j][i]) / 2.0
                    b_tmp += w * (JR.dot(ep))
                b[i] = b_tmp
            for i in fix_handles:
                b[i] = pos_ref[i]

            for i in range(len(m_handles)):
                mi = m_handles[i]
                b[mi] = m_pos_handles[i]

            self.vertices = spsolve(csc_matrix(laplacian), b)


path = 'Bunny_head.obj'
mesh = Mesh(path)
show_obj(mesh)
