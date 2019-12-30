import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def plot_point(ax, point, angle, length):
     x, y = point

     # find the end point
     endy = length * math.sin(math.radians(angle))
     endx = length * math.cos(math.radians(angle))
     m = math.tan(angle)
     print((endx, endy, m, angle))
     ax.plot([x, endx], [y, endy])


if __name__ == "__main__":
     ax = plt.subplot(111)
     ax.set_ylim([0, 50])   # set the bounds to be 10, 10
     ax.set_xlim([0, 50])

     # Change major ticks to show every 5.
     ax.xaxis.set_major_locator(MultipleLocator(1))
     ax.yaxis.set_major_locator(MultipleLocator(1))

     plt.grid()
     plt.step(1, 1)
     plot_point(ax, (0, 0), 50, 100)
     plot_point(ax, (0, 0), 30, 100)
     plt.show()
