import numpy as np
import math
import matplotlib.pyplot as plt
import pylab
from pylab import figure, show, legend
from mpl_toolkits.axes_grid1 import host_subplot

#计算滑动平均值
def moving_avg(interval, p):  
    for i in range(1, len(interval)):
        interval[i] = p * interval[i-1] + (1 - p) * interval[i]
    return interval

r2_list = np.loadtxt("r2_score.txt")
#绘图
x1 = len(r2_list)

#moving average
r2_av = moving_avg(r2_list, 0.9)
x_r2 = range(0, x1)
print(x_r2)

host = host_subplot(111)
plt.subplots_adjust(right=0.8)
host.set_xlabel("iteration")
host.set_ylabel("R2 Score")

p1, = host.plot(x_r2, r2_list, label="test r2 score")

host.legend(loc=5)
host.axis["left"].label.set_color(p1.get_color())

host.set_xlim([-5,525])
plt.draw()
plt.show()