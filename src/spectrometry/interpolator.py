from collections.abc import Iterable
from numbers import Number
from os.path import splitext
import matplotlib.pyplot as plt
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
    x : numpy.ndarray
        The x-coordinates of the data points.
    y : numpy.ndarray
        The y-coordinates of the data points.
    new_x : array-like
        The x-coordinates at which to interpolate.
    new_y : array-like
        The interpolated y-coordinates.

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
        self.new_x, self.new_y = None, None
        self.log_x, self.log_y = None, None
        self.log_new_x, self.log_new_y = None, None

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

    def __call__(self, new_x, method, k=3, log=False):
        return self.interpolate(new_x, method, k=k, log=log)

    def interpolate(self, new_x, methods, k=3, log=False):
        """
        Interpolate the data using the specified methods and store the results.

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
        self.new_x = new_x

        if log:
            self.log_x = np.log(self.x)
            self.log_y = np.log(self.y)
            self.log_new_x = np.log(self.new_x)

        if log:
            x = self.log_x
            y = self.log_y
            new_x = self.log_new_x
        else:
            x = self.x
            y = self.y

        if isinstance(methods, str):
            methods = [methods]

        results = {}
        for method in methods:
            if method == 'PiecewiseLinear':
                new_y = np.interp(new_x, x, y)
            elif method == 'CubicSpline':
                interpolator = CubicSpline(x, y)
                new_y = interpolator(new_x)
            elif method == 'Pchip':
                interpolator = PchipInterpolator(x, y)
                new_y = interpolator(new_x)
            elif method == 'Akima1D':
                interpolator = Akima1DInterpolator(x, y)
                new_y = interpolator(new_x)
            elif method == 'B-splines':
                interpolator = make_interp_spline(x, y, k=k)
                new_y = interpolator(new_x)
            else:
                raise ValueError(f'Invalid interpolation method: {method}. '
                                 f'Valid methods are: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines')
            results[method] = new_y

        if len(results) == 1:
            new_y = next(iter(results.values()))
        else:
            new_y = pd.DataFrame(results)

        if log:
            self.log_new_y = new_y
            self.new_y = np.exp(new_y)
        else:
            self.new_y = new_y

        return self.new_y

    def to_file(self, file_path, csv=True):
        """
        Save the stored interpolation results and the new_x values to a CSV or Excel file.

        Parameters
        ----------
        file_path : str
            The path to the file where the results will be saved.
        csv : bool, optional
            If True, save as CSV; if False, save as Excel. Default is True.

        Raises
        ------
        ValueError
            If no interpolation results are stored.
        """
        if self.new_y is None or self.new_x is None:
            raise ValueError("No interpolation results to save. Please run the interpolate method first.")

        if isinstance(self.new_y, np.ndarray):
            df = pd.DataFrame({'new_x': self.new_x, 'new_y': self.new_y})
        else:
            df = pd.DataFrame(self.new_y)
            df.insert(0, 'new_x', self.new_x)

        if csv:
            df.to_csv(file_path, index=False)
        else:
            df.to_excel(file_path, index=False)

    def plot(self, figsize=(10, 6), show=True, save=False, file_path='interpolation_plot', file_format='png'):
        """
        Plot the interpolation results.

        Parameters
        ----------
        figsize : tuple, optional
            The size of the figure. Default is (10, 6).
        show : bool, optional
            If True, display the plot. Default is True.
        save : bool, optional
            If True, save the plot as a file. Default is False.
        file_path : str, optional
            The path to the file where the plot will be saved. Default is 'interpolation_plot'.
        file_format : str, optional
            The format of the file to save the plot. Default is 'png'.

        Raises
        ------
        ValueError
            If no interpolation results are stored.
        """
        if self.new_y is None or self.new_x is None:
            raise ValueError("No interpolation results to plot. Please run the interpolate method first.")

        plt.figure(figsize=figsize)

        # Plot original data points
        plt.plot(self.x, self.y, 'o', label='Data')

        # Check if new_y is a pandas DataFrame with multiple interpolation methods
        if isinstance(self.new_y, pd.DataFrame):
            for method_name in self.new_y.columns:
                plt.plot(self.new_x, self.new_y[method_name], label=f'{method_name}')
        else:
            # Plot single method interpolation results
            plt.plot(self.new_x, self.new_y, label='Interpolated')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Interpolation Results')
        plt.legend()
        plt.grid(True)

        if save:
            full_file_path = f"{file_path}.{file_format}"
            plt.savefig(full_file_path)
            print(f"Plot saved as {full_file_path}")

        if show:
            plt.show()


def clean_arrays(x, y):
    """
    Clean the input arrays by removing invalid values from y and the corresponding elements from x.

    This function converts the input y array to a numpy array of type float64, checks for invalid values
    (zero, negative, NaN, or infinite values) in y, and removes the invalid elements from both x and y.
    If any invalid values are found, a warning is raised.

    Parameters
    ----------
    x : array-like
        The x-coordinates of the data points.
    y : array-like
        The y-coordinates of the data points.

    Returns
    -------
    tuple of numpy.ndarray
        The cleaned x and y arrays with invalid values removed.

    Raises
    ------
    Warning
        If any invalid values are found in y, a warning is raised and the corresponding elements in x and y are deleted.
    """
    y = np.array(y).astype(np.float64)

    # Check for invalid values in y
    invalid_mask = (y == 0) | (y < 0) | np.isnan(y) | np.isinf(y)

    # If there are any invalid values, raise a warning
    if np.any(invalid_mask):
        warn("Invalid values found in y. Corresponding elements in x and y will be deleted.")

        # Remove invalid elements from x and y
        x = x[~invalid_mask]
        y = y[~invalid_mask]
    else:
        print('no invalid elements')

    return x, y


def interpolate(x, y, new_x, method, k=3):
    """
    Perform interpolation using the specified method.

    This method performs interpolation on the given data using the specified method.

    Parameters
    ----------
    x : numpy.ndarray
        The x-coordinates of the data points to be used for interpolation.
    y : numpy.ndarray
        The y-coordinates of the data points to be used for interpolation.
    new_x : numpy.ndarray
        The x-coordinates at which to interpolate.
    method : str
        The interpolation method to use. Can be one of:
        'PiecewiseLinear', 'CubicSpline', 'Pchip', 'Akima1D', 'B-splines'.
    k : int, optional
        The degree of the spline for 'B-splines' method (default is 3).

    Returns
    -------
    numpy.ndarray
        The interpolated y-coordinates.

    Raises
    ------
    ValueError
        If an invalid interpolation method is provided.
    """
    if method == 'PiecewiseLinear':
        new_y = np.interp(new_x, x, y)
    elif method == 'CubicSpline':
        interpolator = CubicSpline(x, y)
        new_y = interpolator(new_x)
    elif method == 'Pchip':
        interpolator = PchipInterpolator(x, y)
        new_y = interpolator(new_x)
    elif method == 'Akima1D':
        interpolator = Akima1DInterpolator(x, y)
        new_y = interpolator(new_x)
    elif method == 'B-splines':
        interpolator = make_interp_spline(x, y, k=k)
        new_y = interpolator(new_x)
    else:
        raise ValueError(f'Invalid interpolation method: {method}. '
                         f'Valid methods are: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines')
    return new_y


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
# TODO: add support to optional arguments of scipy interpolation methods
# TODO: web app or desktop app?
