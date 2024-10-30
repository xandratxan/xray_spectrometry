from collections.abc import Iterable
from numbers import Number
from os.path import splitext

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline


class Interpolator:
    """
    A class used to perform interpolation.

    Parameters
    ----------
    x : array-like, optional
        The x-coordinates of the data points. Must be provided if `data` is not given.
    y : array-like, optional
        The y-coordinates of the data points. Must be provided if `data` is not given.
    data : array-like, dict, or pandas.DataFrame, optional
        The data points as a list of tuples (x, y), a dictionary with keys 'x' and 'y', or a pandas DataFrame.
        Must be provided if `x` and `y` are not given.

    Attributes
    ----------
    x : array-like
        The x-coordinates of the data points.
    y : array-like
        The y-coordinates of the data points.

    Raises
    ------
    ValueError
        If both `x` and `y` are provided along with `data`.
        If neither `x` and `y` nor `data` are provided.
        If `x`, `y`, or `data` are not non-string iterables.
        If elements of `x`, `y`, or `data` are not numerical.

    Examples
    --------
    >>> interpolator1 = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
    >>> interpolator2 = Interpolator(data={'x': [1, 2, 3], 'y': [4, 5, 6]})
    >>> interpolator3 = Interpolator(data=pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]}))
    >>> interpolator4 = Interpolator(x=[1, 2, 3], y=[4, 5, 6], data=[(1, 4), (2, 5), (3, 6)])
    Traceback (most recent call last):
        ...
    ValueError: Interpolator constructor failed. Provide either 'x' and 'y' or 'data'. Provided Interpolator(x=[1, 2, 3], y=[4, 5, 6], data=[(1, 4), (2, 5), (3, 6)]).
    >>> interpolator5 = Interpolator()
    Traceback (most recent call last):
        ...
    ValueError: Interpolator constructor failed. Provide either 'x' and 'y' or 'data'. Provided Interpolator(x=None, y=None, data=None).
    """

    def __init__(self, x=None, y=None, data=None):
        """
        Initialize the Interpolator with either x and y coordinates or data.

        Parameters
        ----------
        x : array-like, optional
            The x-coordinates of the data points. Must be provided if `data` is not given.
        y : array-like, optional
            The y-coordinates of the data points. Must be provided if `data` is not given.
        data : array-like, dict, or pandas.DataFrame, optional
            The data points as a list of tuples (x, y), a dictionary with keys 'x' and 'y', or a pandas DataFrame.
            Must be provided if `x` and `y` are not given.

        Raises
        ------
        ValueError
            If both `x` and `y` are provided along with `data`.
            If neither `x` and `y` nor `data` are provided.
            If `x`, `y`, or `data` are not non-string iterables.
            If elements of `x`, `y`, or `data` are not numerical.
        """
        self._x, self._y, self._data = x, y, data
        self._validate_arguments_combination()
        self._validate_arguments_type()
        self.x, self.y = self._extract_attributes()
        self._validate_attributes_type()

    def _validate_arguments_combination(self):
        """
        Validate the combination of arguments provided to the constructor.

        Raises
        ------
        ValueError
            If both `x` and `y` are provided along with `data`.
            If neither `x` and `y` nor `data` are provided.
        """
        from_x_y = (self._x is not None and self._y is not None) and self._data is None
        from_data = (self._x is None and self._y is None) and self._data is not None
        if not from_x_y and not from_data:
            raise ValueError("Interpolator constructor failed. Provide either 'x' and 'y' or 'data'.")

    def _validate_arguments_type(self):
        """
        Validate the types of the arguments provided to the constructor.

        Raises
        ------
        ValueError
            If `x`, `y`, or `data` are not non-string iterables.
        """
        for arg in [self._x, self._y, self._data]:
            if arg is not None and not (isinstance(arg, Iterable) and not isinstance(arg, str)):
                raise ValueError("Interpolator constructor failed. Arguments must be non-string iterables.")

    def _extract_attributes(self):
        """
        Extract the x and y attributes from the arguments provided to the constructor.

        Returns
        -------
        x : numpy.ndarray
            The x-coordinates of the data points.
        y : numpy.ndarray
            The y-coordinates of the data points.
        """
        if self._data is not None:
            if isinstance(self._data, dict):
                x, y = np.array(self._data['x']), np.array(self._data['y'])
            elif isinstance(self._data, pd.DataFrame):
                x, y = np.array(self._data.iloc[:, 0]), np.array(self._data.iloc[:, 1])
            else:
                x, y = np.array(self._data[0]), np.array(self._data[1])
        else:
            x, y = np.array(self._x), np.array(self._y)
        return x, y

    def _validate_attributes_type(self):
        """
        Validate the types of the elements of the attributes.

        Raises
        ------
        ValueError
            If elements of `x` or `y` are not numerical.
        """
        for attr in [self.x, self.y]:
            for i in attr:
                if not isinstance(i, Number):
                    raise ValueError("Interpolator constructor failed. Elements of arguments must be numerical.")

    def __repr__(self):
        return f"Interpolator(x={self._x}, y={self._y}, data={self._data})"

    def __str__(self):
        return f"Interpolator with:\nx: {self.x}\ny: {self.y}"

    def __call__(self, new_x, method, k=3):
        return self.interpolate(new_x, method, k=k)

    def interpolate(self, new_x, methods, k=3):
        """
        Interpolate the data using the specified methods.

        Parameters
        ----------
        new_x : array-like
            The x-coordinates at which to interpolate.
        methods : str or list of str
            The interpolation method(s) to use. Can be one or more of:
            'PiecewiseLinear', 'CubicSpline', 'Pchip', 'Akima1D', 'B-splines'.
        k : int, optional
            The degree of the spline for 'B-splines' method (default is 3).

        Returns
        -------
        numpy.ndarray or pandas.DataFrame
            If a single method is provided, returns the interpolated y-coordinates as a numpy array.
            If multiple methods are provided, returns a pandas DataFrame where the columns are the method names
            and the values are the interpolated y-coordinates.

        Raises
        ------
        ValueError
            If an invalid interpolation method is provided.
        """
        if isinstance(methods, str):
            methods = [methods]

        results = {}
        for method in methods:
            if method == 'PiecewiseLinear':
                new_y = np.interp(new_x, self.x, self.y)
            elif method == 'CubicSpline':
                interpolator = CubicSpline(self.x, self.y)
                new_y = interpolator(new_x)
            elif method == 'Pchip':
                interpolator = PchipInterpolator(self.x, self.y)
                new_y = interpolator(new_x)
            elif method == 'Akima1D':
                interpolator = Akima1DInterpolator(self.x, self.y)
                new_y = interpolator(new_x)
            elif method == 'B-splines':
                interpolator = make_interp_spline(self.x, self.y, k=k)
                new_y = interpolator(new_x)
            else:
                raise ValueError(f'Invalid interpolation method: {method}. '
                                 f'Valid methods are: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines')
            results[method] = new_y

        if len(results) == 1:
            return next(iter(results.values()))
        return pd.DataFrame(results)


def read_file(file_path, sheet_name=0, x_col=0, y_col=1, header=True):
    """
    Reads a CSV or Excel file, extracts the specified columns for x and y values, and generates an Interpolator object.

    Parameters
    ----------
    file_path : str
        The path to the file.
    sheet_name : str or int, optional
        The sheet name or index to read from (only used if the file is an Excel file, default is the first sheet).
    x_col : int, optional
        The index of the column containing the x values (default is 0).
    y_col : int, optional
        The index of the column containing the y values (default is 1).
    header : bool, optional
        Whether the first line of the file should be read as a header (default is True).

    Returns
    -------
    Interpolator
        An Interpolator object with the x and y values from the file.

    Raises
    ------
    ValueError
        If the specified columns are not found in the file.
        If the file type is not supported.
    """
    try:
        _, file_extension = splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            df = pd.read_csv(file_path, header=0 if header else None)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=0 if header else None)
        else:
            raise ValueError("Unsupported file type. Must be a CSV or Excel file.")

        if x_col >= len(df.columns) or y_col >= len(df.columns):
            raise ValueError("Specified columns are not found in the file.")

        x = df.iloc[:, x_col].values
        y = df.iloc[:, y_col].values
        return Interpolator(x, y)
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")


# TODO: interpolation in linear or logarithmic scale
# TODO: dealing with zeros or other invalid values in logarithmic scale

# TODO: interpolate a single value or multiple values
# TODO: interpolate using several interpolation methods? compare interpolation results?

# TODO: feature to plot interpolation results?
# TODO: web app or desktop app?
