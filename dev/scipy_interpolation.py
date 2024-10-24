# Script to get familiar with scipy interpolation techniques for one-dimensional data
# References
# https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
# https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=101)

# Piecewise linear interpolation
y_new_linear = np.interp(x_new, x, y)

# Cubic splines
interpolator = CubicSpline(x, y)
y_new_splines = interpolator(x_new)

# Monotone interpolants: Pchip
interpolator = PchipInterpolator(x, y)
y_new_pchip = interpolator(x_new)

# Monotone interpolants: Akima
interpolator = Akima1DInterpolator(x, y)
y_new_akima = interpolator(x_new)

# Interpolation with B-splines (more optional arguments)
interpolator = make_interp_spline(x, y, k=2)
y_new_b_splines = interpolator(x_new)

# Plot the results
plt.plot(x, y, 'o', label='Data')
plt.plot(x_new, y_new_linear, '-', label='Piecewise linear')
plt.plot(x_new, y_new_splines, '-', label='Cubic splines')
plt.plot(x_new, y_new_pchip, '-', label='Monotone: Pchip')
plt.plot(x_new, y_new_akima, '-', label='Monotone: Akima')
plt.plot(x_new, y_new_b_splines, '-', label='B-splines')
plt.legend(loc='best')
plt.show()

names = ['Piecewise linear', 'Cubic splines', 'Monotone: Pchip', 'Monotone: Akima', 'B-splines']
y_new = [y_new_linear, y_new_splines, y_new_pchip, y_new_akima, y_new_b_splines]
fig, ax = plt.subplots(1, len(names), figsize=(16, 3), sharey=True)
for i in range(len(names)):
    print(i, names[i], y_new[i][:3])
    ax[i].plot(x, y, 'o', label='Data')
    ax[i].plot(x_new, y_new[i], '-', label=names[i])
    ax[i].set_title(names[i])
plt.show()
