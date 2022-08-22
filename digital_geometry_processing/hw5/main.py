import  numpy as np
from vispy.io import  read_png
from digital_geometry_processing.utils import rgb_int2rgb,show_obj
import matplotlib.pyplot as plt
import numpy as np
from vispy.io import imread
from vispy.scene.visuals import Mesh
from vispy.visuals.filters import TextureFilter

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
    with open('uv','r') as f:
        for line in f.readlines():
            arr = line.strip().split(' ')
            a = float(arr[0])
            b = float(arr[-1])
            ans.append([a,b])
    return ans

def mat_load():
    ans = []
    with open('mat','r') as f:
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

    def __init__(self,path):
        verts,faces = load_obj(path)
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

            key0 = [index0,index1]
            key1 = [index1,index2]
            key2 = [index2,index0]
            key0.sort()
            key1.sort()
            key2.sort()
            self.edge2faceid[tuple(key0)].add(i)
            self.edge2faceid[tuple(key1)].add(i)
            self.edge2faceid[tuple(key2)].add(i)


        localcoord = []
        total_s = 0
        for i, (v2, v0, v1) in enumerate(self.faces):
            p0 = self.vertices[v0]
            p1 = self.vertices[v1]
            p2 = self.vertices[v2]
            print('p0p1p2',p0,p1,p2)
            total_s += 0.5 * length(cross(p1 - p0, p2 - p0))
            e = p1 - p0
            e2 = p2 - p1
            e2 = normal(e2)
            x_ = normal(e)
            n = cross(e2,x_)
            n = -normal(n)
            y_ = cross(n,x_)
            e1 = p2 - p0
            localcoord.append([0, 0, length(e), 0, dot(e1, x_), dot(e1, y_)])

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
            if v_idx in boundary_vids:
                laplacian0[v_idx][v_idx] = 1
            else:
                for j_idx in self.graph[v_idx]:
                    laplacian0[v_idx][j_idx] = -1
                laplacian0[v_idx][v_idx] = len(self.graph[v_idx])
        N = len(boundary_arr)
        B = np.zeros((len(self.vertices),2))
        delta = np.pi * 2 / N
        for i in range(N):
            ag = delta * i
            vid = boundary_arr[i]
            B[vid][0] = radius * np.cos(ag)
            B[vid][1] = radius * np.sin(ag)
        uv = np.linalg.inv(laplacian0.transpose().dot(laplacian0)).dot(laplacian0.transpose().dot(B))
        # uv = np.linalg.inv(laplacian0).dot(B)
        # uv = np.array(uv_load())
        print('uvvv')
        print(uv)
        edges = self.edge2faceid.keys()
        plot_img(uv, edges)

        # cot
        W = np.zeros((len(self.vertices),len(self.vertices)))
        total_s = 0
        for i, (v2, v0, v1) in enumerate(self.faces):
            p0 = self.vertices[v0]
            p1 = self.vertices[v1]
            p2 = self.vertices[v2]
            angle0 = angle(p1 - p0, p2 - p0)
            angle1 = angle(p0 - p1, p2 - p1)
            angle2 = angle(p0 - p2, p1 - p2)
            total_s += 0.5 * length(cross(p1 - p0, p2 - p0))
            # if v0 not in boundary_vids or v1 not in boundary_vids:
            self.cots[(i, 0)] = 1.0 / np.tan(angle2)
            W[v0][v1] = 1.0 / np.tan(angle2)
            # if v1 not in boundary_vids or v2 not in boundary_vids:
            self.cots[(i, 1)] = 1.0 / np.tan(angle0)
            W[v1][v2] = 1.0 / np.tan(angle0)
            # if v2 not in boundary_vids or v0 not in boundary_vids:
            self.cots[(i, 2)] = 1.0 / np.tan(angle1)
            W[v2][v0] = 1.0 / np.tan(angle1)
        laplacian = np.zeros((len(self.vertices), len(self.vertices)))

        for idx in self.graph:
            ww = 0
            for u in self.graph[idx]:
                # if idx not in boundary_vids or u not in boundary_vids:
                w = W[idx][u] + W[u][idx]
                ww += w
                laplacian[idx][u] = -w
            laplacian[idx][idx] = ww

        laplacian = np.array(mat_load())
        # iterator
        for _ in range(10):
            lts = []
            for i in range(len(self.faces)):
                v2, v0, v1 = self.faces[i]
                P = np.array([
                    [uv[v1][0]-uv[v0][0],uv[v2][0]-uv[v0][0]],
                    [uv[v1][1]-uv[v0][1],uv[v2][1]-uv[v0][1]]
                ])
                S = np.array([
                    [localcoord[i][2]-localcoord[i][0],localcoord[i][4]-localcoord[i][0]],
                    [localcoord[i][3]-localcoord[i][1],localcoord[i][5]-localcoord[i][1]]
                ])
                J = P.dot(np.linalg.inv(S))
                # print('uv0',uv[v0])
                # print('uv1', uv[v1])
                # print('uv2', uv[v2])
                # print('P',P)
                # print('S',S)
                # print('J value',J)

                U,S,V = np.linalg.svd(J)

                R = U.dot(V)

                # print('R', R)
                if np.linalg.det(R) < 0:
                    U[0][1] = -U[0][1]
                    U[1][1] = -U[1][1]
                    R = U.dot(V)
                lts.append(R)

            b = np.zeros((len(self.vertices),2))
            for i in range(len(self.faces)):
                v2, v0, v1 = self.faces[i]

                e0 = np.array([localcoord[i][2] , localcoord[i][3]])
                e1 = np.array([localcoord[i][4] - localcoord[i][2],
                               localcoord[i][5] - localcoord[i][3]])
                e2 = np.array([-localcoord[i][4],-localcoord[i][5]])


                # print('R',lts[i])
                # print('e0',e0,'e1',e1,'e2',e2)
                # print('cots0',self.cots.get((i,0),0))

                b0 = (self.cots.get((i,0),0) * lts[i].dot(e0))
                # print('b0', b0)
                b[v0] -= b0
                b[v1] += b0

                b1 = (self.cots.get((i,1),0) * lts[i].dot(e1))
                b[v1] -= b1
                b[v2] += b1
                # print('cots1', self.cots.get((i, 1), 0))
                # print('b1', b1)

                b2 = (self.cots.get((i,2),0) * lts[i].dot(e2))
                b[v2] -= b2
                b[v0] += b2

                # print('cots2',self.cots.get((i,2),0))
                # print('b2', b2)
            uv = np.linalg.inv(laplacian.transpose().dot(laplacian)).dot(laplacian.transpose().dot(b))
            # uv = np.linalg.inv(laplacian).dot(b)
            # print('A ',np.linalg.det(laplacian))
            # print('b  ',b)
            # print('uv  ',uv)
        plot_img(uv,edges)




def plot_img(x_y_arr,edges):
    x = []
    y = []
    for i,j in x_y_arr:
        x.append(i)
        y.append(j)
    for i,j in edges:
        plt.plot([x_y_arr[i][0],x_y_arr[j][0]],[x_y_arr[i][1],x_y_arr[j][1]])
    # plt.plot(x, y, 'ro')
    plt.show()  # 这个智障的编辑器




path = 'Nefertiti_face.obj'
mesh = Mesh(path)



