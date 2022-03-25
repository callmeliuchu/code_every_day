import numpy as np
from collections import defaultdict

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
    return np.array([ay * bz - az * by, ax * bz - az * bx, ax * by - ay * bx])


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


def colorMap(gaussCur,max,min):
    if gaussCur < 0:
        gaussCur = 1
    return [gaussCur, 0.2, 0.2]


def angle(a, b):
    a = normal(a)
    b = normal(b)
    return np.arccos(a.dot(b))


class Mesh:

    def __init__(self, path):
        self.path = path
        vertices, faces = load_obj(path)
        self.vertices = vertices
        self.faces = faces
        self.norms = [None] * len(faces)
        self.area = [None] * len(faces)
        self.local_area = [0] * len(vertices)
        self.angles = [0] * len(vertices)
        self.v2graph = [[] for _ in range(len(vertices))]
        self.face_angles = defaultdict(float)
        self.edge_cot_angle = defaultdict(float)
        self.graph = defaultdict(set)
        for i in range(len(faces)):
            index0 = faces[i][0]
            index1 = faces[i][1]
            index2 = faces[i][2]
            v01 = self.vertices[index1] - self.vertices[index0]
            v12 = self.vertices[index2] - self.vertices[index1]
            v20 = self.vertices[index0] - self.vertices[index2]
            l01 = length(v01)
            l12 = length(v12)
            l20 = length(v20)
            n0 = cross(v01, v12)
            s = 0.5 * length(n0)
            self.area[i] = s
            n = normal(n0)
            for v in faces[i]:
                self.v2graph[v].append(i)
            if is_dun(v01, -v20):
                s0 = 0.5 * s
                s1 = 0.25 * s
                s2 = 0.25 * s
            elif is_dun(v12, -v01):
                s0 = 0.25 * s
                s1 = 0.5 * s
                s2 = 0.25 * s
            elif is_dun(v20, -v12):
                s0 = 0.25 * s
                s1 = 0.25 * s
                s2 = 0.5 * s
            else:
                ll = l01 + l12 + l20
                s0 = 0.5 * (l01 + l20) / ll * s
                s1 = 0.5 * (l01 + l12) / ll * s
                s2 = 0.5 * (l20 + l12) / ll * s
            self.local_area[index0] += s0
            self.local_area[index1] += s1
            self.local_area[index2] += s2
            angle0 = angle(v01, -v20)
            angle1 = angle(v12, -v01)
            angle2 = angle(v20, -v12)
            self.angles[index0] += angle0
            self.angles[index1] += angle1
            self.angles[index2] += angle2
            self.norms[i] = n
            edge12 = [index1,index2]
            edge10 = [index1,index0]
            edge02 = [index0,index2]
            edge12.sort()
            edge10.sort()
            edge02.sort()
            self.edge_cot_angle[tuple(edge12)] += 1/np.tan(angle0)
            self.edge_cot_angle[tuple(edge10)] += 1 / np.tan(angle2)
            self.edge_cot_angle[tuple(edge02)] += 1 / np.tan(angle1)
            self.graph[index0].add(index1)
            self.graph[index0].add(index2)
            self.graph[index1].add(index0)
            self.graph[index1].add(index2)
            self.graph[index2].add(index1)
            self.graph[index2].add(index0)
        self.colors = []
        # for i in range(len(vertices)):
        #     v = np.array([0.0,0.0,0.0])
        #     for j in self.graph[i]:
        #         key = [i,j]
        #         key.sort()
        #         key = tuple(key)
        #         # print(self.edge_cot_angle[key])
        #         # print(vertices[i]-vertices[j])
        #         v += self.edge_cot_angle[key]*(vertices[i]-vertices[j])
        #     v = v / self.local_area[i]
        #     self.colors.append(length(v))



        for i in range(len(vertices)):
            self.colors.append(1/self.local_area[i]*(2*np.pi-self.angles[i]))

        max_c = max(self.colors)
        min_c = min(self.colors)
        self.colors = [colorMap(c,max_c,min_c) for c in self.colors]

