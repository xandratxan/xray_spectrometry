import numpy as np
import pandas as pd

from spectrometry.interpolator import Interpolator

# print('Valid definitions')
#
# print("Interpolator from x and y")
# # From two lists
# interpolator10 = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
# # From two tuples
# interpolator11 = Interpolator(x=(1, 2, 3), y=(4, 5, 6))
# # From two 1D NumPy arrays
# interpolator12 = Interpolator(x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
# # From two Pandas Series
# interpolator13 = Interpolator(x=pd.Series([1, 2, 3]), y=pd.Series([4, 5, 6]))
#
# print("Interpolator from data")
# # From a list of two lists
# interpolator20 = Interpolator(data=[[1, 2, 3], [4, 5, 6]])
# # From a list of two tuples
# interpolator21 = Interpolator(data=[(1, 2, 3), (4, 5, 6)])
# # From a list of two 2D numpy arrays
# interpolator22 = Interpolator(data=[np.array([1, 2, 3]), np.array([4, 5, 6])])
# # From a tuple of two tuples
# interpolator23 = Interpolator(data=((1, 2, 3), (4, 5, 6)))
# # From a tuple of two lists
# interpolator24 = Interpolator(data=([1, 2, 3], [4, 5, 6]))
# # From a tuple of two 2D numpy arrays
# interpolator25 = Interpolator(data=(np.array([1, 2, 3]), np.array([4, 5, 6])))
# # From a 2D numpy arrays
# interpolator26 = Interpolator(data=np.array([[1, 2, 3], [4, 5, 6]]))
# # From a dictionary with keys x and y
# interpolator27 = Interpolator(data={'x': [1, 2, 3], 'y': [4, 5, 6]})
# # From a 2x2 pandas dataframe with x in the first column and y in the second column
# interpolator28 = Interpolator(data=pd.DataFrame(data={'x': [1, 2, 3], 'y': [4, 5, 6]}))

print("Invalid argument type")

# interpolator03 = Interpolator(x='hello', y='world')
# y_new = interpolator03(0.5, 'CubicSpline')

# interpolator04 = Interpolator(data='hello')
# y_new = interpolator04(0.5, 'CubicSpline')

# interpolator05 = Interpolator(x=1, y=2)
# y_new = interpolator05(0.5, 'CubicSpline')

# interpolator06 = Interpolator(data=3)
# y_new = interpolator06(0.5, 'CubicSpline')

# interpolator07 = Interpolator(x=['a', 2, 3], y=[4, 5, 6])
# y_new = interpolator07(0.5, 'CubicSpline')

# interpolator08 = Interpolator(x=[1, 2, 3], y=['a', 5, 6])
# y_new = interpolator08(0.5, 'CubicSpline')
try:
    interpolator09 = Interpolator(data=[['a', 2, 3], [4, 5, 6]])
    y_new = interpolator09(0.5, 'CubicSpline')
except Exception as e:
    print(f'{type(e)}: {e}')
