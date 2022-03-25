from vispy import scene


def show_obj(mesh):
    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    verts = mesh.vertices
    faces = mesh.faces
    colors = mesh.colors

    mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                              vertex_colors=colors)

    view.add(mesh)

    view.camera = scene.TurntableCamera()
    view.camera.depth_value = 10

    canvas.app.run()
