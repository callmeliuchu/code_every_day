import numpy as np
from numpy import argmin
from scipy import bincount
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d

def cvt(num):
    p = np.random.random((num,2))
    piece_num = 30
    n = (piece_num+1)*(piece_num+1)
    grid = np.zeros((n,2))
    k = 0
    sx = []
    sy = []

    for i in range(piece_num+1):
        for j in range(piece_num+1):
            x = i/piece_num
            y = j/piece_num
            grid[k] = np.array([x,y])
            sx.append(x)
            sy.append(y)
            k += 1
    it = 100
    for j in range(it):
        if j % 10 == 0:
            # vor = Voronoi(p)
            # voronoi_plot_2d(vor)
            tri = Delaunay(p)
            plt.triplot(p[:,0],p[:,1],tri.simplices.copy())
            plt.title('Iteration Time: ' + str(it))
            plt.show()

        print(p)
        grid_classify = [argmin([(g-pp).dot(g-pp) for pp in p]) for g in grid]
        count = bincount(grid_classify,[1]*len(grid_classify))
        new_x = bincount(grid_classify,sx)
        new_y = bincount(grid_classify,sy)
        print(grid_classify)
        print(count)
        print(new_x)
        print(new_y)
        for index,c in enumerate(count):
            if c > 0:
                new_x[index] = new_x[index]/float(c)
                new_y[index] = new_y[index]/float(c)
        p[:,0] = new_x[:]
        p[:,1] = new_y[:]


cvt(30)
