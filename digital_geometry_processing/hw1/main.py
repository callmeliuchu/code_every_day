from vispy import scene
from digital_geometry_processing.hw1.mesh import Mesh



canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()





mesh = Mesh(
    "/Users/liuchu/code_every_day/digital_geometry_processing/hw2/PumpkinMesh.obj")

# mesh = Mesh('/Users/liuchu/Digital_Geometry_Processing/code/example/hw4/cow.obj')

# mesh = Mesh('/Users/liuchu/Digital_Geometry_Processing/code/example/hw3/bunny_random.obj')

# mesh = Mesh('/Users/liuchu/Digital_Geometry_Processing/code/example/hw6/Bunny_head.obj')


verts = mesh.vertices
faces = mesh.faces
colors = mesh.colors

print(mesh.angles)

mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                          vertex_colors=colors)

view.add(mesh)

view.camera = scene.TurntableCamera()
view.camera.depth_value = 10

if __name__ == '__main__':
    canvas.app.run()
