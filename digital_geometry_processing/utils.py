from vispy import scene



def show_obj(mesh):
    canvas = scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    verts = mesh.vertices
    faces = mesh.faces
    if hasattr(mesh,'colors'):
        colors = mesh.colors


        m = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                              vertex_colors=colors,color='white')
    else:
        m = scene.visuals.Mesh(vertices=verts, faces=faces, shading='smooth',
                               color='white')

    if hasattr(mesh,'texture_filter'):

        m.attach(mesh.texture_filter)

    view.add(m)

    view.camera = scene.TurntableCamera()
    view.camera.depth_value = 20

    canvas.app.run()


def rgb_int2rgb(rgbint):
    r = rgbint // 256 // 256 % 256
    g = rgbint // 256 % 256
    b = rgbint % 256
    return [r/256,0,b/256]






