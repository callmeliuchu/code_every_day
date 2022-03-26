import  numpy as np
from digital_geometry_processing.utils import rgb_int2rgb,show_obj


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
    y = (x-min)/(max-min)*(2**24-1)
    return rgb_int2rgb(y)


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

    def get_vector(self):
        return self.v2.point - self.v1.point

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


class Mesh:

    def __init__(self,path):
        verts,faces = load_obj(path)
        self.vertices = verts
        self.faces = faces
        self.half_edge = HalfEdge(verts,faces)
        self.boundaries = self.half_edge.find_boundary()
        self.local_area = [0]*len(self.vertices)
        for face in self.half_edge.faces:
            self.get_local_area(face.edge)
        lap = self.cal_laplacian()
        # print(lap)
        # for _ in range(1000):
        #     for i in range(len(self.vertices)):
        #         self.vertices[i] -= 0.001*lap[i]
        colors = [length(v) for v in lap]
        print(colors)
        max_c = max(colors)
        min_c = min(colors)
        colors = [colorMap(c,max_c,min_c) for c in colors]
        print(colors)
        self.colors = colors


    def cal_laplacian(self):
        ans = []
        for i in range(len(self.vertices)):
            if i in self.boundaries:
                ans.append(np.array([0.0,0.0,0.0]))
                continue
            res = np.array([0.0,0.0,0.0])
            edge = self.half_edge.vertices[i].edge
            p = edge
            while True:
                w = self.get_cot_edge(p)
                res += w*p.get_vector()
                p = p.opposite.next_edge
                if p is edge:
                    break
            res = res/4/self.local_area[p.v1.id]
            ans.append(res)
        return ans



    def get_cot_edge(self,p):
        e1 = p.next_edge
        e2 = e1.next_edge
        a1 = self.get_angle(e1,e2)

        e3 = p.opposite.next_edge
        e4 = e3.next_edge
        a2 = self.get_angle(e3,e4)

        return 1/np.tan(a1) + 1/np.tan(a2)


    def get_angle(self,e1,e2):
        return angle(e1.get_vector(),-e2.get_vector())


    def get_local_area(self,p):
        v01 = p.get_vector()
        v12 = p.next_edge.get_vector()
        v20 = p.next_edge.next_edge.get_vector()
        l01 = length(v01)
        l12 = length(v12)
        l20 = length(v20)
        v_index0 = p.v1.id
        v_index1 = p.v2.id
        v_index2 = p.next_edge.v2.id
        n0 = cross(v01, v12)
        s = 0.5 * length(n0)
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
        self.local_area[v_index0] += s0
        self.local_area[v_index1] += s1
        self.local_area[v_index2] += s2








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
    path = '/Users/liuchu/code_every_day/digital_geometry_processing/hw2/PumpkinMesh.obj'
    verts,faces = load_obj(path)
    he = HalfEdge(verts,faces)
    print(he)
    print(he.find_adj_verts(0))
    print(he.faces[0])
    print(he.faces[1])
    print(he.find_boundary())
    mesh = Mesh(path)
    show_obj(mesh)


ff()
