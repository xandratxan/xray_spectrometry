from spectrometry import Interpolator
import numpy as np
import matplotlib.pyplot as plt

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)

# Define an interpolator
interpolator = Interpolator(x, y)

# Piecewise linear interpolation
x_new = np.linspace(0, 10, num=101)
y_new_multiple = interpolator(x_new, 'PiecewiseLinear')

# Piecewise linear interpolation
x_new = 5.5
y_new_single = interpolator(x_new, 'PiecewiseLinear')
