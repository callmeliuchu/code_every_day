from collections import defaultdict
import numpy as np
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



if __name__ == '__main__':

    mesh = Mesh(
        "/Users/liuchu/code_every_day/digital_geometry_processing/hw8/result/7.obj")
    show_obj(mesh)
