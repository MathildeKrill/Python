import numpy
import matplotlib.pyplot as plt
mu = - 0.2
limit = 1
xvalues, yvalues = numpy.meshgrid(numpy.arange(-limit, limit, 0.1), 
                                  numpy.arange(-limit, limit, 0.1))
xdot = mu * xvalues - yvalues + xvalues * yvalues * yvalues
ydot = mu * yvalues + xvalues + yvalues * yvalues * yvalues
plt.streamplot(xvalues, yvalues, xdot, ydot)
plt.grid()
plt.show()