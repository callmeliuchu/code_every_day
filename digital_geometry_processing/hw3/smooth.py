from digital_geometry_processing.hw3.mesh import Mesh
from digital_geometry_processing.utils import show_obj
path = '/Users/liuchu/code_every_day/digital_geometry_processing/hw3/bunny_random.obj'

path = '/Users/liuchu/Digital_Geometry_Processing/code/example/hw6/Bunny_head.obj'
# path = '/Users/liuchu/Digital_Geometry_Processing/code/example/hw9/dragon.obj'
mesh = Mesh(path)


show_obj(mesh)
