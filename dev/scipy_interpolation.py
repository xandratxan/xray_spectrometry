# Script to get familiar with scipy interpolation techniques for one-dimensional data
# References
# https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
# https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html

import numpy as np
import matplotlib.pyplot as plt

# Piecewise linear interpolation

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=21)
print(x)
print(y)
print(x_new)

# Interpolate
y_new = np.interp(x_new, x, y)
print(y_new)

# Plot the results
plt.plot(x_new, y_new, '-', label='Linear')
plt.plot(x, y, 'o', label='Data')
plt.legend(loc='best')
plt.show()

# Cubic splines

# Monotone interpolants

# Interpolation with B-splines

# Parametric spline curves
