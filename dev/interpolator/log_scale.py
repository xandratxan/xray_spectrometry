from spectrometry import Interpolator
import numpy as np
import matplotlib.pyplot as plt

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = [1,2,3]
y = [10,20,30]
x_new = [1.5, 2.5]

# Define an interpolator
interpolator_lin = Interpolator(x, y)
# Linear scale
y_new_lin = interpolator_lin(x_new, 'PiecewiseLinear', log=False)

# Define an interpolator
interpolator_log = Interpolator(x, y)
# Logarithmic scale
y_new_log = interpolator_log(x_new, 'PiecewiseLinear', log=True)

# Define an interpolator
interpolator_lin_m = Interpolator(x, y)
# Linear scale
y_new_lin_m = interpolator_lin_m(x_new, ['PiecewiseLinear', 'CubicSpline'], log=False)

# Define an interpolator
interpolator_log_m = Interpolator(x, y)
# Logarithmic scale
y_new_log_m = interpolator_log_m(x_new, ['PiecewiseLinear', 'CubicSpline'], log=True)