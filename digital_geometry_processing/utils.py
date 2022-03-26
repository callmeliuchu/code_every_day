from vispy import scene


def show_obj(mesh):
    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    verts = mesh.vertices
    faces = mesh.faces
    if hasattr(mesh,'colors'):
        colors = mesh.colors


        mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                              vertex_colors=colors)
    else:
        mesh = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                                  )

    view.add(mesh)

    view.camera = scene.TurntableCamera()
    view.camera.depth_value = 10

    canvas.app.run()


def rgb_int2rgb(rgbint):
    r = rgbint // 256 // 256 % 256
    g = rgbint // 256 % 256
    b = rgbint % 256
    return [r/256,0,b/256]






