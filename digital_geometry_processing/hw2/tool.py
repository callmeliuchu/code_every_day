import numpy as np
from matplotlib import cm, colors
values = np.linspace(0.0, 3.0, 10)
norm = colors.Normalize(vmin=1.0, vmax=2.0, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.Greys_r)
for value in values:
   print("%.2f" % value, "=",
      "red:%.2f" % mapper.to_rgba(value)[0],
      "green:%.2f" % mapper.to_rgba(value)[1],
      "blue:%.2f" % mapper.to_rgba(value)[2])
