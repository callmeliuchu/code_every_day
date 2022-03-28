from digital_geometry_processing.utils import show_obj
from digital_geometry_processing.hw1.mesh import Mesh

if __name__ == '__main__':

    mesh = Mesh(
        "/Users/liuchu/code_every_day/digital_geometry_processing/hw2/PumpkinMesh.obj")
    show_obj(mesh)
