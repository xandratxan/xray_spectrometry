# Script to get familiar with scipy interpolation techniques for one-dimensional data
# References
# https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
# https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html

import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=101)

# Piecewise linear interpolation
y_new_linear = np.interp(x_new, x, y)

# Cubic splines
interpolator_splines = CubicSpline(x, y)
y_new_splines = interpolator_splines(x_new)

# Monotone interpolants

# Interpolation with B-splines

# Parametric spline curves

# Plot the results
plt.plot(x, y, 'o', label='Data')
plt.plot(x_new, y_new_linear, '-', label='Piecewise linear')
plt.plot(x_new, y_new_splines, '-', label='Cubic splines')
plt.legend(loc='best')
plt.show()