import numpy as np
import pandas as pd

from spectrometry import Interpolator

print("Script to show the initialization of an Interpolator")

print("Invalid arguments combinations")
try:
    interpolator01 = Interpolator()
except ValueError as e:
    print(e)
try:
    interpolator01a = Interpolator(x=[1, 2, 3], data=[[1, 2, 3], [4, 5, 6]])
except ValueError as e:
    print(e)
try:
    interpolator01b = Interpolator(y=[1, 2, 3], data=[[1, 2, 3], [4, 5, 6]])
except ValueError as e:
    print(e)
try:
    interpolator02 = Interpolator(x=[1, 2, 3], y=[4, 5, 6], data=[[1, 2, 3], [4, 5, 6]])
except ValueError as e:
    print(e)

print("Invalid argument type")
try:
    interpolator03 = Interpolator(x='hello', y='world')
except ValueError as e:
    print(e)
try:
    interpolator04 = Interpolator(data='hello')
except ValueError as e:
    print(e)
try:
    interpolator05 = Interpolator(x=1, y=2)
except ValueError as e:
    print(e)
try:
    interpolator06 = Interpolator(data=3)
except ValueError as e:
    print(e)

print("Invalid type in iterable argument")
try:
    interpolator07 = Interpolator(x=['a', 2, 3], y=[4, 5, 6])
except ValueError as e:
    print(e)
try:
    interpolator08 = Interpolator(x=[1, 2, 3], y=['a', 5, 6])
except ValueError as e:
    print(e)
try:
    interpolator09 = Interpolator(data=[['a', 2, 3], [4, 5, 6]])
except ValueError as e:
    print(e)

print("Interpolator from x and y")
# From two lists
interpolator10 = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
# From two tuples
interpolator11 = Interpolator(x=(1, 2, 3), y=(4, 5, 6))
# From two 1D NumPy arrays
interpolator12 = Interpolator(x=np.array([1, 2, 3]), y=np.array([4, 5, 6]))
# From two Pandas Series
interpolator13 = Interpolator(x=pd.Series([1, 2, 3]), y=pd.Series([4, 5, 6]))

print("Interpolator from data")
# From a list of two lists
interpolator20 = Interpolator(data=[[1, 2, 3], [4, 5, 6]])
# From a list of two tuples
interpolator21 = Interpolator(data=[(1, 2, 3), (4, 5, 6)])
# From a list of two 2D numpy arrays
interpolator22 = Interpolator(data=[np.array([1, 2, 3]), np.array([4, 5, 6])])
# From a tuple of two tuples
interpolator23 = Interpolator(data=((1, 2, 3), (4, 5, 6)))
# From a tuple of two lists
interpolator24 = Interpolator(data=([1, 2, 3], [4, 5, 6]))
# From a tuple of two 2D numpy arrays
interpolator25 = Interpolator(data=(np.array([1, 2, 3]), np.array([4, 5, 6])))
# From a 2D numpy arrays
interpolator26 = Interpolator(data=np.array([[1, 2, 3], [4, 5, 6]]))
# From a dictionary with keys x and y
interpolator27 = Interpolator(data={'x': [1, 2, 3], 'y': [4, 5, 6]})
# From a 2x2 pandas dataframe with x in the first column and y in the second column
interpolator28 = Interpolator(data=pd.DataFrame(data={'x': [1, 2, 3], 'y': [4, 5, 6]}))
