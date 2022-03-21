from vispy import scene, io

from .graph import Graph

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()

verts, faces, normals, nothing = io.read_mesh("/Users/liuchu/Digital_Geometry_Processing/code/example/hw1/alien.obj")

mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth')

view.add(mesh)
G = Graph(verts, faces)
points, faces1 = G.shortest_path(4234, 9894)

line = scene.visuals.Line(pos=points, color=(0.8, 0.2, 0.1, 1))
view.add(line)

view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()
