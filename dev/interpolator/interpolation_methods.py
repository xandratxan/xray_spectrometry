from spectrometry import Interpolator
import numpy as np
import matplotlib.pyplot as plt

# Define data to interpolate
# - Two arrays of data to interpolate, x, and y
# - A third array, xnew, of points to evaluate the interpolation on
x = np.linspace(0, 10, num=11)
y = np.cos(-x ** 2 / 9.0)
x_new = np.linspace(0, 10, num=101)

# # Define an interpolator
# i = Interpolator(x, y)
# # Piecewise linear interpolation
# y_new_linear = i.interpolate(x_new, 'PiecewiseLinear')
# # Cubic splines
# y_new_splines = i.interpolate(x_new, 'CubicSpline')
# # Monotone interpolants: Pchip
# y_new_pchip = i.interpolate(x_new, 'Pchip')
# # Monotone interpolants: Akima
# y_new_akima = i.interpolate(x_new, 'Akima1D')
# # Interpolation with B-splines (more optional arguments)
# y_new_b_splines = i.interpolate(x_new, 'B-splines')

# Define an interpolator
interpolator = Interpolator(x, y)
# Piecewise linear interpolation
y_new_linear = interpolator(x_new, 'PiecewiseLinear')
# Cubic splines
y_new_splines = interpolator(x_new, 'CubicSpline')
# Monotone interpolants: Pchip
y_new_pchip = interpolator(x_new, 'Pchip')
# Monotone interpolants: Akima
y_new_akima = interpolator(x_new, 'Akima1D')
# Interpolation with B-splines (more optional arguments)
y_new_b_splines = interpolator(x_new, 'B-splines')

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
