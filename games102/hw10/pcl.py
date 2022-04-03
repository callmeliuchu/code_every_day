import numpy as np
import vispy.scene
from vispy.scene import visuals
import sys


# Make a canvas and add simple view
canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()



# # generate data  使用随机数据的话把这块反注释掉
# pos = np.random.normal(size=(100000, 3), scale=0.2)
# # one could stop here for the data generation, the rest is just to make the
# # data look more interesting. Copied over from magnify.py
# centers = np.random.normal(size=(50, 3))
# indexes = np.random.normal(size=100000, loc=centers.shape[0]/2.,
#                            scale=centers.shape[0]/3.)
# indexes = np.clip(indexes, 0, centers.shape[0]-1).astype(int)
# scales = 10**(np.linspace(-2, 0.5, centers.shape[0]))[indexes][:, np.newaxis]
# pos *= scales
# pos += centers[indexes]
# scatter = visuals.Markers()
# scatter.set_data(pos, edge_color=None, face_color=(1, 1, 1, .5), size=5)

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


# 使用 kitti 数据， n*3
img_id = 17  # 2，3 is not able for pcl;

points,_ = load_obj('/Users/liuchu/code_every_day/digital_geometry_processing/hw2/PumpkinMesh.obj')



# create scatter object and fill in the data
scatter = visuals.Markers()
scatter.set_data(points[:,:3], edge_color=None, face_color=(1, 1, 1, .5), size=5)

view.add(scatter)
view.camera = 'turntable'  # or try 'arcball'

# add a colored 3D axis for orientation
axis = visuals.XYZAxis(parent=view.scene)


if __name__ == '__main__':
    if sys.flags.interactive != 1:
        vispy.app.run()
