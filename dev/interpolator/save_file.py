from spectrometry import Interpolator
import numpy as np

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=101)

# Define an interpolator
interpolator = Interpolator(x, y)

# Piecewise linear interpolation
y_new = interpolator(x_new, 'PiecewiseLinear')
# Save to csv
interpolator.to_file("./results.csv")
# Save to excel
interpolator.to_file("./results.xlsx")

# Piecewise linear interpolation and Cubic splines
y_new = interpolator.interpolate(x_new, ['PiecewiseLinear', 'CubicSpline'])
# Save to csv
interpolator.to_file("./results.csv")
# Save to excel
interpolator.to_file("./results.xlsx")