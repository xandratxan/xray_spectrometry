import numpy as np
import scipy as sp

class Interpolator:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self, new_x, method):
        return self.interpolate(new_x, method)

    def interpolate(self, new_x, method):
        if method=='PiecewiseLinear':
            new_y = np.interp(new_x, self.x, self.y)
            return new_y
        elif method=='CubicSpline':
            interpolator = sp.interpolate.CubicSpline(self.x, self.y)
            new_y = interpolator(new_x)
            return new_y
        elif method=='Pchip':
            interpolator = sp.interpolate.PchipInterpolator(self.x, self.y)
            new_y = interpolator(new_x)
            return new_y
        elif method=='Akima1D':
            interpolator = sp.interpolate.Akima1DInterpolator(self.x, self.y)
            new_y = interpolator(new_x)
            return new_y
        elif method=='B-splines':
            interpolator = sp.interpolate.make_interp_spline(self.x, self.y, k=2)
            new_y = interpolator(new_x)
            return new_y
        else:
            raise ValueError(f'Interpolation methods: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines')

