import numpy as np
from spectrometry.interpolator import interpolate, Interpolator

# Sample data points
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 16, 25])
new_x = np.linspace(0, 5, 50)

# Example 1: Piecewise Linear Interpolation with optional arguments
new_y_linear = interpolate(x, y, new_x, 'PiecewiseLinear', left=-1, right=26)
print("Piecewise Linear Interpolation:", new_y_linear)

# Example 2: Cubic Spline Interpolation with optional arguments
new_y_cubic = interpolate(x, y, new_x, 'CubicSpline', bc_type='natural', extrapolate=True)
print("Cubic Spline Interpolation:", new_y_cubic)

# Example 3: Pchip Interpolation with optional arguments
new_y_pchip = interpolate(x, y, new_x, 'Pchip', extrapolate=True)
print("Pchip Interpolation:", new_y_pchip)

# Example 4: Akima1D Interpolation with optional arguments
new_y_akima = interpolate(x, y, new_x, 'Akima1D', method='makima', extrapolate=True)
print("Akima1D Interpolation:", new_y_akima)

# Example 5: B-splines Interpolation with optional arguments
new_y_bspline = interpolate(x, y, new_x, 'B-splines', k=3, bc_type='clamped')
print("B-splines Interpolation:", new_y_bspline)


# Example 1: Piecewise Linear Interpolation with optional arguments
new_y_linear = Interpolator(x, y).interpolate(new_x, 'PiecewiseLinear', left=-1, right=26)
print("Piecewise Linear Interpolation:", new_y_linear)

# Example 2: Cubic Spline Interpolation with optional arguments
new_y_cubic = Interpolator(x, y).interpolate(new_x, 'CubicSpline', bc_type='natural', extrapolate=True)
print("Cubic Spline Interpolation:", new_y_cubic)

# Example 3: Pchip Interpolation with optional arguments
new_y_pchip = Interpolator(x, y).interpolate(new_x, 'Pchip', extrapolate=True)
print("Pchip Interpolation:", new_y_pchip)

# Example 4: Akima1D Interpolation with optional arguments
new_y_akima = Interpolator(x, y).interpolate(new_x, 'Akima1D', method='makima', extrapolate=True)
print("Akima1D Interpolation:", new_y_akima)

# Example 5: B-splines Interpolation with optional arguments
new_y_bspline = Interpolator(x, y).interpolate(new_x, 'B-splines', k=3, bc_type='clamped')
print("B-splines Interpolation:", new_y_bspline)


interpolator = Interpolator(x, y)

# Example 1: Piecewise Linear Interpolation with optional arguments
new_y_linear = interpolator(new_x, 'PiecewiseLinear', left=-1, right=26)
print("Piecewise Linear Interpolation:", new_y_linear)

# Example 2: Cubic Spline Interpolation with optional arguments
new_y_cubic = interpolator(new_x, 'CubicSpline', bc_type='natural', extrapolate=True)
print("Cubic Spline Interpolation:", new_y_cubic)

# Example 3: Pchip Interpolation with optional arguments
new_y_pchip = interpolator(new_x, 'Pchip', extrapolate=True)
print("Pchip Interpolation:", new_y_pchip)

# Example 4: Akima1D Interpolation with optional arguments
new_y_akima = interpolator(new_x, 'Akima1D', method='makima', extrapolate=True)
print("Akima1D Interpolation:", new_y_akima)

# Example 5: B-splines Interpolation with optional arguments
new_y_bspline = interpolator(new_x, 'B-splines', k=3, bc_type='clamped')
print("B-splines Interpolation:", new_y_bspline)