from digital_geometry_processing.utils import show_obj
from digital_geometry_processing.hw6.mesh import Mesh

if __name__ == '__main__':

    mesh = Mesh(
        "Bunny_head.obj")
    show_obj(mesh)
