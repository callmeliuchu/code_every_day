import matplotlib.pyplot as plt
import numpy as np
import heapq
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


def colorMap(x, max, min):
    # y = (x-min)/(max-min)*(2**24-1)
    # return rgb_int2rgb(y)
    return [x / max * 1.5, 0.1, 0.2]


def angle(a, b):
    a = normal(a)
    b = normal(b)
    return np.arccos(a.dot(b))

class Vertex:

    def __init__(self,v_id,point):
        self.id = v_id
        self.edge = None
        self.point = point

    def __repr__(self):
        return 'id:{}'.format(self.id)


class Edge:

    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2
        self.next_edge = None
        self.pre_edge = None
        self.opposite = None
        self.face = None

    def __repr__(self):
        return '{} --> {}'.format(self.v1,self.v2)


class Face:

    def __init__(self,edge):
        self.edge = edge

    def __repr__(self):
        return str(self.edge)


class HalfEdge:

    def __init__(self,verts,fs):
        self.points = verts
        self.vertices = []
        for i,point in enumerate(verts):
            self.vertices.append(Vertex(i,point))
        self.faces = []
        self.edges_cache = {}
        self.connect(fs)

    def create_edge(self,v1,v2):
        v1_id = v1.id
        v2_id = v2.id
        key1 = (v1_id,v2_id)
        key2 = (v2_id,v1_id)
        if key1 not in self.edges_cache:
            self.edges_cache[key1] = Edge(v1,v2)
        if key2 not in self.edges_cache:
            self.edges_cache[key2] = Edge(v2,v1)
        self.edges_cache[key1].opposite = self.edges_cache[key2]
        self.edges_cache[key2].opposite = self.edges_cache[key1]
        return self.edges_cache[key1]

    def connect(self,fs):
        for f in fs:
            edges = []
            for i in range(3):
                edge = self.create_edge(self.vertices[f[i]],self.vertices[f[(i+1)%3]])
                self.vertices[f[i]].edge = edge
                edges.append(edge)

            face = Face(edges[0])
            self.faces.append(face)
            for i in range(3):
                edges[i].next_edge = edges[(i+1)%3]
                edges[(i + 1) % 3].pre_edge = edges[i]
                edges[i].face = face

    def find_adj_verts(self,v_id):
        v = self.vertices[v_id]
        edge = v.edge
        p = edge
        ans = []
        # while edge is not None and edge is not p:
        #     ans.append(edge.v2)
        #     edge = edge.opposite.next_edge
        # while True:
        #     if p.next_edge is None and p is not edge:
        #         break
        #     p = p.next_edge.next_edge
        #     p = p.opposite
        #     ans.append(p.v2)
        return ans

    def find_boundary(self):
        ans = []
        for key in self.edges_cache:
            if self.edges_cache[key].next_edge is None:
                ans.extend(key)
        return set(ans)

    def get_boundary_edge(self):
        mapping = {}
        p = None
        for key in self.edges_cache:
            if self.edges_cache[key].next_edge is None:
                v1,v2 = key
                mapping[v1] = v2
                if p is None:
                    p = v1
        p = list(self.find_boundary())[-1]
        ans = []
        s = 0
        if p is not None:
            q = p
            before = None
            while p in mapping:
                if before is None:
                    ans.append([p,s])
                else:
                    s += length(self.points[before]-self.points[p])
                    ans.append([p,s])
                before = p
                p = mapping[p]
                if p == q:
                    break
            s += length(self.points[ans[-1][0]]-self.points[q])
        return ans,s

    def boundary2square(self):
        indexes, l = self.get_boundary_edge()
        def f(x):
            if 0 <= x <= l/4:
                return [x,0]
            elif l/4 <= x <= l/2:
                return [l/4,x-l/4]
            elif l/2 <= x <= 3*l/4:
                return [3*l/4-x,l/4]
            elif 3*l/4 <= x <= l:
                return [0,l-x]
        ans = {}
        count = 0
        for index,x in indexes:
            ans[index] = [4*v/l for v in f(l*count/len(indexes))]
            count += 1
        for k,v in ans.items():
            print(k,v)
        return ans




def clamp(val):
    return val
    # if val < 0:
    #     return 0
    # if val > 1:
    #     return 1
    # return val




class Mesh:

    def __init__(self,path):
        # verts,faces = load_obj(path)
        verts = [[i*1.0+np.random.random(),i*1.0,i*1.0+np.random.random()] for i in range(9)]
        faces = [
            [2,0,3],
            [0,2,4],
            [0,4,5],
            [0,5,1],
            [0,1,3],
            [1,5,6],
            [1,6,7],
            [1,7,8],
            [1,8,3],
        ]
        verts = np.array(verts)
        faces = np.array(faces)
        # verts, faces = load_obj(path)
        self.vertices = verts
        self.faces = faces
        self.cal_graph_edges()
        self.deleted_vertices = [0]*len(self.vertices)
        self.deleted_faces = [0] * len(self.faces)



    def cal_graph_edges(self):
        self.edges = []
        self.graph = defaultdict(set)
        self.vertice2face = defaultdict(list)
        for f,face in enumerate(self.faces):
            i,j,k = face
            self.graph[i].add(j)
            self.graph[i].add(k)
            self.graph[j].add(i)
            self.graph[j].add(k)
            self.graph[k].add(i)
            self.graph[k].add(j)
            self.vertice2face[i].append(f)
            self.vertice2face[j].append(f)
            self.vertice2face[k].append(f)
            e1 = [i,j]
            e2 = [j,k]
            e3 = [k,i]
            for e in [e1,e2,e3]:
                e.sort()
                e = tuple(e)
                self.edges.append(e)
        self.edges = set(self.edges)



    def cal_abcd(self,face):
        index0 = face[0]
        index1 = face[1]
        index2 = face[2]
        v01 = self.vertices[index1] - self.vertices[index0]
        v12 = self.vertices[index2] - self.vertices[index1]
        v20 = self.vertices[index0] - self.vertices[index2]
        n0 = cross(v01, v12)
        n0 = normal(n0)
        a,b,c = n0
        d = -n0.dot(self.vertices[index1])
        return a,b,c,d

    def generate_mat(self,face):
        a,b,c,d = self.cal_abcd(face)
        v1 = np.array([[a,b,c,d]]).transpose()
        v2 = v1.transpose()
        return v1 * v2

    def cal_every_point_mat(self):
        ans = [np.zeros((4,4)) for _ in range(len(self.vertices))]
        for face_id,face in enumerate(self.faces):
            if self.deleted_faces[face_id] == 0:
                mat = self.generate_mat(face)
                for index in face:
                    ans[index] += mat
        return ans

    def cal_every_edge(self):
        point_mat = self.cal_every_point_mat()
        heap = []
        for v1,v2 in self.edges:
            q = point_mat[v1] + point_mat[v2]
            q[3,:] = np.array([0.0,0.0,0.0,1.0])
            s = np.linalg.det(q)
            if s == 0:
                v = (self.vertices[v1]+self.vertices[v2])/2
            else:
                m = np.linalg.inv(q)
                v = m.dot(np.array([0,0,0,1.0]).transpose())
                v = v / v[-1]
                v = v[:3]
            vv = np.array(list(v) + [1.0])
            cost = vv.dot(q).dot(vv.transpose())
            heapq.heappush(heap,[cost,[(v1,v2),v]])
        while heap:
            c,item = heapq.heappop(heap)
            edge,point = item
            v0,v1 = edge
            #更新完权重
            self.merge_two_vertices(v0,v1,point)
            v_set = set()
            for face_id in self.vertice2face[v0]:
                if self.deleted_faces[face_id] == 0:
                    for p in self.faces[face_id]:
                        if self.deleted_vertices[p] == 0:
                            v_set.add(p)
            for i in v_set:
                point_mat[i] = np.zeros((4,4))
            for i in v_set:
                for face_id in self.vertice2face[i]:
                    face = self.faces[face_id]
                    point_mat[i] += self.generate_mat(face)
            for i in v_set:
                if i != v0:
                    if self.deleted_vertices[i] == 1 or self.deleted_vertices[v0] == 1:
                        continue
                    q = point_mat[v0] + point_mat[i]
                    q[3, :] = np.array([0.0, 0.0, 0.0, 1.0])
                    s = np.linalg.det(q)
                    if s == 0:
                        v = (self.vertices[v0] + self.vertices[i]) / 2
                    else:
                        m = np.linalg.inv(q)
                        v = m.dot(np.array([0, 0, 0, 1.0]).transpose())[:3]
                    vv = np.array(list(v) + [1.0])
                    cost = vv.dot(q).dot(vv.transpose())
                    print(cost,type(cost))
                    heapq.heappush(heap, [cost, [(v0, i), v]])





    def merge_two_vertices(self,v0,v1,point):
        #删除顶点
        self.deleted_vertices[v1] = 1
        self.vertices[v0] = np.array(point)
        for face_id in self.vertice2face[v1]:
            face = self.faces[face_id]
            #删除对应顶点的face
            self.deleted_faces[face_id] = 1
            i,j,k = face
            new_face = [i,j,k]
            v1_index = new_face.index(v1)
            new_face[v1_index] = v0
            if new_face.count(v0) == 2:
                continue
            else:
                # 合法的face覆盖原来的face
                self.deleted_faces[face_id] = 0
                self.faces[face_id] = new_face
        #重新生成v0对应的face
        v0_faces = []
        for face_id in self.vertice2face[v1] + self.vertice2face[v0]:
            if self.deleted_faces[face_id] == 0:
                v0_faces.append(face_id)
        self.vertice2face[v0] = v0_faces





def plot_img(x_y_arr,edges):
    x = []
    y = []
    for i,j in x_y_arr:
        x.append(i)
        y.append(j)
    for i,j in edges:
        plt.plot([x_y_arr[i][0],x_y_arr[j][0]],[x_y_arr[i][1],x_y_arr[j][1]])
    # plt.plot(x, y, 'ro')
    plt.show()



def ff():

    # verts = [
    #     [0,1,2],
    #     [2,3,5],
    #     [4,5,6],
    #     [5,6,8],
    #     [5,63,4]
    # ]
    #
    #
    # facs = [
    #     [2,1,0],
    #     [2,0,3]
    # ]
    #
    path = '/Users/liuchu/code_every_day/games102/hw7/Nefertiti_face.obj'
    verts,faces = load_obj(path)



# mesh = Mesh('/Users/liuchu/code_every_day/games102/hw7/Nefertiti_face.obj')
mesh = Mesh('/Users/liuchu/code_every_day/digital_geometry_processing/hw2/PumpkinMesh.obj')
mesh.cal_every_edge()
# mesh.merge_two_vertices(0,1,[0.5,0.5,0.5])


