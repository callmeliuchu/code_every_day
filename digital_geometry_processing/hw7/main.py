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

        total_s = 0
        for i, (v0, v1, v2) in enumerate(self.faces):
            p0 = self.vertices[v0]
            p1 = self.vertices[v1]
            p2 = self.vertices[v2]
            total_s += 0.5 * length(cross(p1 - p0, p2 - p0))





        # uv
        radius = np.sqrt(total_s / np.pi)
        boundary_link = defaultdict(list)
        boundary_vids = set()
        for key in self.edge2faceid:
            if len(self.edge2faceid[key]) == 1:
                boundary_vids.add(key[0])
                boundary_vids.add(key[1])
                boundary_link[key[0]].append(key[1])
                boundary_link[key[1]].append(key[0])


        def cal_wij(v0,v1,v2):
            alpha1 = angle(v0,v1)
            alpha2 = angle(v0,v2)
            return (np.tan(alpha1/2) + np.tan(alpha2/2))/length(v0)

        W = np.zeros((len(self.vertices), len(self.vertices)))
        for vid in self.graph:
            if vid not in boundary_vids:
                total_w = 0
                for j in self.graph[vid]:
                    edge = [vid,j]
                    edge.sort()
                    edge = tuple(edge)
                    f1_id,f2_id = self.edge2faceid[edge]
                    f1 = self.faces[f1_id]
                    f2 = self.faces[f2_id]
                    other1 = None
                    for o in f1:
                        if o not in edge:
                            other1 = o
                    other2 = None
                    for o in f2:
                        if o not in edge:
                            other2 = o
                    v0 = self.vertices[j] - self.vertices[vid]
                    v1 = self.vertices[other1] - self.vertices[vid]
                    v2 = self.vertices[other2] - self.vertices[vid]
                    wij = cal_wij(v0,v1,v2)
                    W[vid][j] = -wij
                    total_w += wij
                W[vid][vid] = total_w
                W[vid] /= total_w

        start = list(boundary_vids)[0]
        visited = set()
        boundary_arr = [start]
        while len(visited) < len(boundary_vids):
            if start not in visited:
                visited.add(start)
                for u in boundary_link[start]:
                    if u not in visited:
                        boundary_arr.append(u)
                        start = u
        laplacian0 = np.zeros((len(self.vertices),len(self.vertices)))
        for v_idx in self.graph:
            for j_idx in self.graph[v_idx]:
                laplacian0[v_idx][j_idx] = W[v_idx][j_idx]
            laplacian0[v_idx][v_idx] = 1
        N = len(boundary_arr)
        B = np.zeros((len(self.vertices),2))
        delta = np.pi * 2 / N
        for i in range(N):
            ag = delta * i
            vid = boundary_arr[i]
            B[vid][0] = radius * np.cos(ag)
            B[vid][1] = radius * np.sin(ag)
        uv = np.linalg.inv(laplacian0.transpose().dot(laplacian0)).dot(laplacian0.transpose().dot(B))
        plot_img(uv, self.edge2faceid.keys())

def plot_img(x_y_arr,edges):
    x = []
    y = []
    for i,j in x_y_arr:
        x.append(i)
        y.append(j)
    for i,j in edges:
        plt.plot([x_y_arr[i][0],x_y_arr[j][0]],[x_y_arr[i][1],x_y_arr[j][1]])
    plt.show()



path = 'Nefertiti_face.obj'
mesh = Mesh(path)
