from collections import defaultdict
import numpy as np
from vispy import scene



def show_obj():

    path = "/Users/liuchu/Digital_Geometry_Processing/code/build/result/0.000000.obj"
    pp = '/Users/liuchu/Digital_Geometry_Processing/code/build/result'

    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    for p in os.listdir(pp):
        pppp = pp + '/' + p
        v,f = load_obj(pppp)
        m = scene.visuals.Mesh(vertices=v, faces=f, shading='smooth',
                               color='white')
        view.add(m)
        view.camera = scene.TurntableCamera()
        view.camera.depth_value = 20
        canvas.show()




def rgb_int2rgb(rgbint):
    r = rgbint // 256 // 256 % 256
    g = rgbint // 256 % 256
    b = rgbint % 256
    return [r/256,0,b/256]









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


import os
import time
if __name__ == '__main__':

    show_obj()
