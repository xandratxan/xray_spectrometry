from spectrometry import Interpolator
import numpy as np

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=101)

# # Define an interpolator
interpolator = Interpolator(x, y)

# # Piecewise linear interpolation and Cubic splines
y_new_single = interpolator.interpolate(x_new, 'PiecewiseLinear')
# # Plot interpolation results
interpolator.plot(save=True, file_path='single')

# Piecewise linear interpolation and Cubic splines
y_new_multiple = interpolator.interpolate(x_new, ['PiecewiseLinear', 'CubicSpline'])
# Plot interpolation results
interpolator.plot(save=True, file_path='multiple')
