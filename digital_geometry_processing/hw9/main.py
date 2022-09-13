import numpy as np
import copy
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
        self.vert2faceid = defaultdict(set)
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

            self.vert2faceid[index0].add(i)
            self.vert2faceid[index1].add(i)
            self.vert2faceid[index2].add(i)

        boundary_link = defaultdict(list)
        boundary_vids = set()
        for key in self.edge2faceid:
            if len(self.edge2faceid[key]) == 1:
                boundary_vids.add(key[0])
                boundary_vids.add(key[1])
                boundary_link[key[0]].append(key[1])
                boundary_link[key[1]].append(key[0])

        self.boundary_vids = boundary_vids

Q = {}
State = {}
Cost = []

def cal_cost(mesh,edge):
    v0,v1 = edge
    Q_solve = Q[v0] + Q[v1]
    Q_plus = copy.deepcopy(Q_solve)
    Q_plus[3][0] = 0
    Q_plus[3][1] = 0
    Q_plus[3][2] = 0
    Q_plus[3][3] = 1
    if np.linalg.det(Q_solve) == 0:

        tmp = (mesh.vertices[v0] + mesh.vertices[v1])/2
        new_vec = np.array([tmp[0],tmp[1],tmp[2],1.0])
    else:
        Q_solve_ = np.linalg.inv(Q_solve)

        new_vec = np.array([Q_solve_[3][0],Q_solve_[3][1],Q_solve_[3][2],Q_solve_[3][3]])
        tmp = new_vec[:3]

    cost = {
        "cost" : new_vec.T.dot(Q_plus).dot(new_vec),
        "eh" : edge,
        "state" : State[edge],
        "new_point" : tmp
    }
    Cost.append(cost)


def collapse(tmp,mesh):
    pass


def qem(mesh):
    nv = len(mesh.vertices)
    if nv == 3:
        return

    for i in range(nv):
        p = mesh.vertices[i]
        Q_tmp = np.zeros((4,4))
        for face_id in mesh.vert2faceid[i]:
            face = mesh.faces[face_id]
            v0,v1,v2 = face
            v01 = mesh.vertices[v1] - mesh.vertices[v0]
            v12 = mesh.vertices[v2] - mesh.vertices[v1]
            nor = cross(v01,v12)
            nor = normal(nor)
            a,b,c = nor
            d = -dot(nor,p)
            V = np.array([[a,b,c,d]])
            VT = V.T
            Q_tmp += VT * V
        Q[i] = Q_tmp

    for edge in mesh.edge2faceid:
        State[edge] = 0
        cal_cost(mesh,edge)

    target_num = min(int(0.5*nv),1000)

    while nv > target_num:
        tmp = Cost.top()
        eh = tmp['eh']
        if tmp['state'] == State[eh]:

            if eh.index != -1:
                collapse(tmp,mesh)
                nv -= 1






