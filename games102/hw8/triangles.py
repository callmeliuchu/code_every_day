import triangle as tri
import matplotlib.pyplot as plt


face = tri.get_data('box.3')
# face.pop('holes')
t=tri.triangulate(face,'pc')
tri.compare(plt,face,t)
plt.show()
