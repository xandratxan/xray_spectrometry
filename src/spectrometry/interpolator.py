from warnings import warn
from collections.abc import Iterable
from numbers import Number
from os.path import splitext

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline

from dev.interpolator.interpolation_methods import x_new


class Interpolator:
    """
    Interpolator class for performing various interpolation methods on given data.

    This class provides functionality to initialize with x and y coordinates or a data structure containing them,
    validate the input, perform interpolation using different methods, and save or plot the results.

    Parameters
    ----------
    x : array-like, optional
        The x-coordinates of the data points. Default is None.
    y : array-like, optional
        The y-coordinates of the data points. Default is None.
    data : dict, pandas.DataFrame, or list of array-like, optional
        The data containing x and y coordinates. If provided, `x` and `y` should be None. Default is None.

    Attributes
    ----------
    x : numpy.ndarray
        The x-coordinates of the data points.
    y : numpy.ndarray
        The y-coordinates of the data points.
    new_x : numpy.ndarray or None
        The x-coordinates for which interpolation is performed.
    new_y : numpy.ndarray or pandas.DataFrame or None
        The interpolated y-coordinates.
    log_x : numpy.ndarray or None
        The logarithm of the x-coordinates of the data points.
    log_y : numpy.ndarray or None
        The logarithm of the y-coordinates of the data points.
    log_new_x : numpy.ndarray or None
        The logarithm of the x-coordinates for which interpolation is performed.
    log_new_y : numpy.ndarray or None
        The logarithm of the interpolated y-coordinates.

    Methods
    -------
    interpolate(new_x, methods, k=3, log=False)
        Perform interpolation using one or more specified methods.
    to_file(file_path, csv=True)
        Save the interpolation results to a file.
    plot(fig_size=(10, 6), show=True, save=False, file_path='interpolation_plot', file_format='png')
        Plot the interpolation results.

    Raises
    ------
    ValueError
        If neither `x` and `y` nor `data` are provided, or if both are provided.
        If the provided arguments are not non-string iterables.
        If the elements of `x` or `y` are not numerical.
        If there are no interpolation results to save (in `to_file` method).
        If there are no interpolation results to plot (in `plot` method).
    """

    def __init__(self, x=None, y=None, data=None):
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

        This method checks if the combination of arguments provided to the constructor is valid.
        It ensures that either 'x' and 'y' are provided together, or 'data' is provided, but not both.

        Raises
        ------
        ValueError
            If neither 'x' and 'y' nor 'data' are provided.
            If both 'x' and 'y' and 'data' are provided.
        """
        from_x_y = (self._x is not None and self._y is not None) and self._data is None
        from_data = (self._x is None and self._y is None) and self._data is not None
        if not from_x_y and not from_data:
            raise ValueError("Interpolator constructor failed. Provide either 'x' and 'y' or 'data'.")

    def _validate_arguments_type(self):
        """
        Validate the types of arguments provided to the constructor.

        This method checks if the arguments provided to the constructor are non-string iterables.
        It ensures that 'x', 'y', and 'data' (if provided) are non-string iterables.

        Raises
        ------
        ValueError
            If any of the arguments are not non-string iterables.
        """
        for arg in [self._x, self._y, self._data]:
            if arg is not None and not (isinstance(arg, Iterable) and not isinstance(arg, str)):
                raise ValueError("Interpolator constructor failed. Arguments must be non-string iterables.")

    def _extract_attributes(self):
        """
        Extract the x and y attributes from the arguments provided to the constructor.

        This method extracts the x and y attributes from the provided data.
        If 'data' is provided, it extracts 'x' and 'y' from the data.
        If 'x' and 'y' are provided, it converts them to numpy arrays.

        Returns
        -------
        tuple of numpy.ndarray
            The extracted x and y attributes as numpy arrays.

        Raises
        ------
        ValueError
            If the data format is invalid.
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
        Validate the types of the extracted attributes.

        This method checks if the extracted attributes 'x' and 'y' are numerical.
        It ensures that all elements in 'x' and 'y' are instances of the Number class.

        Raises
        ------
        ValueError
            If any element in 'x' or 'y' is not numerical.
        """
        for attr in [self.x, self.y]:
            if not is_1d_numeric_array(attr):
                raise ValueError("Interpolator constructor failed. Attributes x and y must be one-dimensional numeric NumPy arrays.")

    def __repr__(self):
        """
        Return a string representation of the Interpolator object.

        This method returns a string representation of the Interpolator object,
        including the initial x, y, and data attributes provided to the constructor.

        Returns
        -------
        str
            A string representation of the Interpolator object.
        """
        return f"Interpolator(x={self._x}, y={self._y}, data={self._data})"

    def __str__(self):
        """
        Return a string representation of the Interpolator object.

        This method returns a string representation of the Interpolator object,
        including the extracted x and y attributes.

        Returns
        -------
        str
            A string representation of the Interpolator object.
        """
        return f"Interpolator with:\nx: {self.x}\ny: {self.y}"

    def __call__(self, new_x, methods, log=False, **kwargs):
        """
        Interpolate the data using the specified method when the object is called.

        This method allows the Interpolator object to be called as a function to perform interpolation.
        It uses the specified method to interpolate the data at the given new_x values.

        Parameters
        ----------
        new_x : array-like
            The x-coordinates at which to interpolate.
        methods : str
            The interpolation method to use. Can be one of:
            'PiecewiseLinear', 'CubicSpline', 'Pchip', 'Akima1D', 'B-splines'.
        log : bool, optional
            If True, apply logarithmic transformation to the data before interpolation. Default is False.
        **kwargs : dict, optional
            Additional keyword arguments to pass to the interpolation methods.

        Returns
        -------
        numpy.ndarray or pandas.DataFrame
            The interpolated y-coordinates.
        """
        return self.interpolate(new_x, methods, log=log, **kwargs)

    def interpolate(self, new_x, algorithms, log=False, **kwargs):
        """
        Interpolate the data using the specified methods and store the results.

        Parameters
        ----------
        new_x : array-like
            The x-coordinates at which to interpolate.
        algorithms : str or list of str
            The interpolation method(s) to use. Can be one or more of:
            'PiecewiseLinear', 'CubicSpline', 'Pchip', 'Akima1D', 'B-splines'.
        log : bool, optional
            If True, apply logarithmic transformation to the data before interpolation. Default is False.
        **kwargs : dict, optional
            Additional keyword arguments to pass to the interpolation methods.

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
        if log:
            self.x, self.y = clean_arrays(self.x, self.y)

        self._set_interpolation_attr(new_x, log)

        x, y, new_x = self._get_interpolation_data(log)

        if isinstance(algorithms, str):
            algorithms = [algorithms]

        results = {}
        for algorithm in algorithms:
            new_y = interpolate(x, y, new_x, algorithm, **kwargs)
            results[algorithm] = new_y

        if len(results) == 1:
            new_y = next(iter(results.values()))
        else:
            new_y = pd.DataFrame(results)

        self._set_interpolated_attr(new_y, log)

        return self.new_y

    def _set_interpolation_attr(self, new_x, log):
        """
        Set the attributes for interpolation.

        This method sets the attributes required for interpolation, including the new x-coordinates
        and optionally applies a logarithmic transformation to the x and y data.

        Parameters
        ----------
        new_x : array-like
            The x-coordinates at which to interpolate.
        log : bool
            If True, apply logarithmic transformation to the data before interpolation.

        Raises
        ------
        ValueError
            If `new_x` is not a non-string iterable.
            If elements of `new_x` are not numerical.
        """
        if isinstance(new_x, Number):
            new_x = [new_x]
        if not is_1d_numeric_array(x_new):
            raise ValueError("Interpolation failed. New x-coordinates must be a one-dimensional numeric NumPy array.")
        self.new_x = new_x
        if log:
            self.log_x = np.log(self.x)
            self.log_y = np.log(self.y)
            self.log_new_x = np.log(self.new_x)

    def _get_interpolation_data(self, log):
        """
        Get the appropriate x, y, and new_x data based on the scale.

        This method returns the original or logarithmically transformed data based on the value of the log parameter.

        Parameters
        ----------
        log : bool
            If True, return the logarithmically transformed data. Otherwise, return the original data.

        Returns
        -------
        tuple of numpy.ndarray
            The x, y, and new_x data to be used for interpolation.
        """
        if log:
            return self.log_x, self.log_y, self.log_new_x
        else:
            return self.x, self.y, self.new_x

    def _set_interpolated_attr(self, new_y, log):
        """
        Sets the interpolated attribute values.

        Parameters
        ----------
        new_y : array-like
            The interpolated y-values.
        log : bool
            If True, the interpolated values are in logarithmic scale.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If `new_y` is None or not an array-like object.

        Notes
        -----
        This method updates the instance attributes `new_y` and `log_new_y` based on the interpolation results.
        If `log` is True, exponential transformation is applied to `new_y` to revert the logarithmic transformation.
        """
        if log:
            self.log_new_y = new_y
            self.new_y = np.exp(new_y)
        else:
            self.new_y = new_y

    def to_file(self, file_path, csv=True):
        """
        Save the interpolation results to a file.

        Parameters
        ----------
        file_path : str
            The path to the file where the results will be saved.
        csv : bool, optional
            If True, save the results as a CSV file. If False, save as an Excel file. Default is True.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If there are no interpolation results to save (i.e., `new_y` or `new_x` is None).

        Notes
        -----
        This method saves the interpolated x and y values to a specified file. The file format can be either CSV or Excel.
        If the interpolated results are stored in a DataFrame, the new x values are inserted as the first column.
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

    def plot(self, fig_size=(10, 6), show=True, save=False, file_path='interpolation_plot', file_format='png'):
        """
        Plot the interpolation results.

        Parameters
        ----------
        fig_size : tuple of int, optional
            The size of the figure (width, height) in inches. Default is (10, 6).
        show : bool, optional
            If True, display the plot. Default is True.
        save : bool, optional
            If True, save the plot to a file. Default is False.
        file_path : str, optional
            The path to the file where the plot will be saved. Default is 'interpolation_plot'.
        file_format : str, optional
            The format of the file to save the plot. Default is 'png'.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If there are no interpolation results to plot (i.e., `new_y` or `new_x` is None).

        Notes
        -----
        This method plots the original data points and the interpolated results. If multiple interpolation methods are used,
        each method's results are plotted with a different label. The plot can be displayed, saved to a file, or both.
        """
        if self.new_y is None or self.new_x is None:
            raise ValueError("No interpolation results to plot. Please run the interpolate method first.")

        plt.figure(figsize=fig_size)

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

    return x, y


def interpolate(x, y, new_x, algorithm, **kwargs):
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
    algorithm : str
        The interpolation method to use. Can be one of:
        'PiecewiseLinear', 'CubicSpline', 'Pchip', 'Akima1D', 'B-splines'.
    **kwargs : dict, optional
        Additional keyword arguments to pass to the interpolation methods.

    Returns
    -------
    numpy.ndarray
        The interpolated y-coordinates.

    Raises
    ------
    ValueError
        If an invalid interpolation method is provided.
    """
    method_kwargs = {
        'PiecewiseLinear': ['left', 'right', 'period'],
        'CubicSpline': ['axis', 'bc_type', 'extrapolate'],
        'Pchip': ['axis', 'extrapolate'],
        'Akima1D': ['axis', 'method', 'extrapolate'],
        'B-splines': ['k', 't', 'bc_type', 'axis', 'check_finite']
    }

    if algorithm not in method_kwargs:
        raise ValueError(f'Invalid interpolation method: {algorithm}. '
                         f'Valid methods are: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines')

    # Filter kwargs to pass only the relevant ones for the chosen method
    filtered_kwargs = {key: value for key, value in kwargs.items() if key in method_kwargs[algorithm]}

    if algorithm == 'PiecewiseLinear':
        new_y = np.interp(new_x, x, y, **filtered_kwargs)
    elif algorithm == 'CubicSpline':
        interpolator = CubicSpline(x, y, **filtered_kwargs)
        new_y = interpolator(new_x)
    elif algorithm == 'Pchip':
        interpolator = PchipInterpolator(x, y, **filtered_kwargs)
        new_y = interpolator(new_x)
    elif algorithm == 'Akima1D':
        interpolator = Akima1DInterpolator(x, y, **filtered_kwargs)
        new_y = interpolator(new_x)
    elif algorithm == 'B-splines':
        interpolator = make_interp_spline(x, y, **filtered_kwargs)
        new_y = interpolator(new_x)

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
        If there is an error reading the file.
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


def is_1d_numeric_array(arr):
    """
    Check if the input is a one-dimensional NumPy array with all numeric elements.

    Parameters
    ----------
    arr : any
        The input to check.

    Returns
    -------
    bool
        True if the input is a one-dimensional NumPy array with all numeric elements, False otherwise.
    """
    # Check if the input is a NumPy array
    if not isinstance(arr, np.ndarray):
        return False

    # Check if the array is one-dimensional
    if arr.ndim != 1:
        return False

    # Check if all elements are numeric
    if not np.issubdtype(arr.dtype, np.number):
        return False

    return True

# TODO: In docstrings: detailed description or notes?
# TODO: Docs: line comments to explain the code
