import os
from io import StringIO
from tempfile import NamedTemporaryFile

import numpy as np
import pandas as pd
import pytest
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline

from src.spectrometry.interpolator import Interpolator, read_file, interpolate, clean_arrays


class TestInterpolator:
    class TestConstructor:
        class TestInitialization:
            def test_valid_x_y(self):
                interpolator = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

            def test_valid_data_dict(self):
                data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
                interpolator = Interpolator(data=data)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

            def test_valid_data_dataframe(self):
                data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
                interpolator = Interpolator(data=data)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

            def test_valid_array(self):
                data = np.array([[1, 2, 3], [4, 5, 6]])
                interpolator = Interpolator(data=data)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

            def test_invalid_both_x_y_and_data(self):
                with pytest.raises(ValueError, match="Provide either 'x' and 'y' or 'data'"):
                    Interpolator(x=[1, 2, 3], y=[4, 5, 6], data=[(1, 4), (2, 5), (3, 6)])

            def test_invalid_neither_x_y_nor_data(self):
                with pytest.raises(ValueError, match="Provide either 'x' and 'y' or 'data'"):
                    Interpolator()

        class TestArgumentTypes:
            def test_invalid_x_type(self):
                with pytest.raises(ValueError, match="Arguments must be non-string iterables"):
                    Interpolator(x="invalid", y=[4, 5, 6])

            def test_invalid_y_type(self):
                with pytest.raises(ValueError, match="Arguments must be non-string iterables"):
                    Interpolator(x=[1, 2, 3], y="invalid")

            def test_invalid_data_type(self):
                with pytest.raises(ValueError, match="Arguments must be non-string iterables"):
                    Interpolator(data="invalid")

        class TestElementTypes:
            def test_invalid_x_element_type(self):
                with pytest.raises(ValueError, match="Elements of arguments must be numerical"):
                    Interpolator(x=[1, 2, "invalid"], y=[4, 5, 6])

            def test_invalid_y_element_type(self):
                with pytest.raises(ValueError, match="Elements of arguments must be numerical"):
                    Interpolator(x=[1, 2, 3], y=[4, 5, "invalid"])

            def test_invalid_data_element_type(self):
                data = {'x': [1, 2, 3], 'y': [4, 5, "invalid"]}
                with pytest.raises(ValueError, match="Elements of arguments must be numerical"):
                    Interpolator(data=data)

    class TestStringRepresentations:
        def test_repr(self):
            interpolator = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
            assert repr(interpolator) == "Interpolator(x=[1, 2, 3], y=[4, 5, 6], data=None)"

        def test_str(self):
            interpolator = Interpolator(x=[1, 2, 3], y=[4, 5, 6])
            assert str(interpolator) == "Interpolator with:\nx: [1 2 3]\ny: [4 5 6]"

    class TestSetInterpolationAttr:
        def setup_method(self):
            # Setup common test data
            self.x = np.array([1, 2, 3, 4, 5])
            self.y = np.array([2, 4, 6, 8, 10])
            self.new_x = np.array([1.5, 2.5, 3.5])
            self.interpolator = Interpolator(x=self.x, y=self.y)

        def test_set_interpolation_attr_log_true(self):
            # Test with log=True
            self.interpolator._set_interpolation_attr(self.new_x, log=True)
            assert np.array_equal(self.interpolator.new_x, self.new_x)
            assert np.array_equal(self.interpolator.log_x, np.log(self.x))
            assert np.array_equal(self.interpolator.log_y, np.log(self.y))
            assert np.array_equal(self.interpolator.log_new_x, np.log(self.new_x))

        def test_set_interpolation_attr_log_false(self):
            # Test with log=False
            self.interpolator._set_interpolation_attr(self.new_x, log=False)
            assert np.array_equal(self.interpolator.new_x, self.new_x)
            assert self.interpolator.log_x is None
            assert self.interpolator.log_y is None
            assert self.interpolator.log_new_x is None

        def test_set_interpolation_attr_invalid_new_x_str(self):
            # Test with invalid new_x (non-string iterable)
            with pytest.raises(ValueError):
                self.interpolator._set_interpolation_attr('hello', log=False)

        def test_set_interpolation_attr_invalid_new_x_non_numeric(self):
            # Test with invalid new_x (non-numeric)
            with pytest.raises(ValueError):
                self.interpolator._set_interpolation_attr(['a', 'b', 'c'], log=False)

    class TestGetInterpolationData:
        def setup_method(self):
            # Setup common test data
            self.x = np.array([1, 2, 3, 4, 5])
            self.y = np.array([2, 4, 6, 8, 10])
            self.new_x = np.array([1.5, 2.5, 3.5])
            self.interpolator = Interpolator(x=self.x, y=self.y)

        def test_get_interpolation_data_log_false(self):
            # Test with log=False
            self.interpolator._set_interpolation_attr(self.new_x, log=False)
            x, y, new_x = self.interpolator._get_interpolation_data(log=False)
            assert np.array_equal(x, self.x)
            assert np.array_equal(y, self.y)
            assert np.array_equal(new_x, self.new_x)

        def test_get_interpolation_data_log_true(self):
            # Test with log=True
            self.interpolator._set_interpolation_attr(self.new_x, log=True)
            log_x, log_y, log_new_x = self.interpolator._get_interpolation_data(log=True)
            assert np.array_equal(log_x, np.log(self.x))
            assert np.array_equal(log_y, np.log(self.y))
            assert np.array_equal(log_new_x, np.log(self.new_x))

    class TestSetInterpolatedAttr:
        def setup_method(self):
            # Setup common test data
            self.x = np.array([1, 2, 3, 4, 5])
            self.y = np.array([2, 4, 6, 8, 10])
            self.new_x = np.array([1.5, 2.5, 3.5])
            self.new_y = np.array([3, 5, 7])
            self.interpolator = Interpolator(x=self.x, y=self.y)

        def test_set_interpolated_attr_log_true(self):
            # Test with log=True
            self.interpolator._set_interpolated_attr(np.log(self.new_y), log=True)
            assert np.array_equal(self.interpolator.log_new_y, np.log(self.new_y))
            assert np.allclose(self.interpolator.new_y, self.new_y)

        def test_set_interpolated_attr_log_false(self):
            # Test with log=False
            self.interpolator._set_interpolated_attr(self.new_y, log=False)
            assert np.array_equal(self.interpolator.new_y, self.new_y)
            assert self.interpolator.log_new_y is None

    class TestToFile:
        def setup_method(self):
            # Setup common test data
            self.x = np.array([1, 2, 3, 4, 5])
            self.y = np.array([2, 4, 6, 8, 10])
            self.new_x = np.array([1.5, 2.5, 3.5])
            self.new_y = np.array([3, 5, 7])
            self.interpolator = Interpolator(x=self.x, y=self.y)
            self.interpolator.new_x = self.new_x
            self.interpolator.new_y = self.new_y
            self.csv_file_path = 'test_interpolation.csv'
            self.excel_file_path = 'test_interpolation.xlsx'

        def teardown_method(self):
            # Remove test files if they exist
            if os.path.exists(self.csv_file_path):
                os.remove(self.csv_file_path)
            if os.path.exists(self.excel_file_path):
                os.remove(self.excel_file_path)

        def test_to_file_no_interpolation_results(self):
            # Test saving without interpolation results
            interpolator = Interpolator(x=self.x, y=self.y)
            with pytest.raises(ValueError):
                interpolator.to_file(self.csv_file_path, csv=True)

        def test_to_file_csv(self):
            # Test saving to CSV file
            self.interpolator.to_file(self.csv_file_path, csv=True)
            assert os.path.exists(self.csv_file_path)
            df = pd.read_csv(self.csv_file_path)
            assert np.array_equal(df['new_x'].values, self.new_x)
            assert np.array_equal(df['new_y'].values, self.new_y)

        def test_to_file_excel(self):
            # Test saving to Excel file
            self.interpolator.to_file(self.excel_file_path, csv=False)
            assert os.path.exists(self.excel_file_path)
            df = pd.read_excel(self.excel_file_path)
            assert np.array_equal(df['new_x'].values, self.new_x)
            assert np.array_equal(df['new_y'].values, self.new_y)

        def test_to_file_dataframe_new_y(self):
            # Test saving when new_y is a DataFrame
            self.interpolator.new_y = pd.DataFrame({'method1': self.new_y, 'method2': self.new_y + 1})
            self.interpolator.to_file(self.csv_file_path, csv=True)
            assert os.path.exists(self.csv_file_path)
            df = pd.read_csv(self.csv_file_path)
            assert np.array_equal(df['new_x'].values, self.new_x)
            assert np.array_equal(df['method1'].values, self.new_y)
            assert np.array_equal(df['method2'].values, self.new_y + 1)

    class TestInterpolate:
        def setup_method(self):
            # Setup common test data
            self.x = np.array([1, 2, 3, 4, 5])
            self.y = np.array([2, 4, 6, 8, 10])
            self.new_x = np.array([1.5, 2.5, 3.5])
            self.expected_y = np.array([3, 5, 7])
            self.interpolator = Interpolator(x=self.x, y=self.y)

        def test_interpolate_single_method_linear_scale(self):
            # Test single interpolation method in linear scale
            new_y = self.interpolator.interpolate(self.new_x, 'PiecewiseLinear')
            assert np.array_equal(new_y, self.expected_y)

        def test_interpolate_single_method_log_scale(self):
            # Test single interpolation method in logarithmic scale
            new_y = self.interpolator.interpolate(self.new_x, 'PiecewiseLinear', log=True)
            assert np.allclose(new_y, self.expected_y)

        def test_interpolate_single_method_linear_scale(self):
            # Test multiple interpolation methods in linear scale
            new_y = self.interpolator.interpolate(self.new_x, ['PiecewiseLinear', 'CubicSpline'])
            assert np.array_equal(new_y['PiecewiseLinear'], self.expected_y)
            assert np.array_equal(new_y['CubicSpline'], self.expected_y)


class TestReadFile:
    class TestCSV:
        def test_valid_csv_with_header(self):
            csv_data = "x,y\n1,4\n2,5\n3,6"
            df = pd.read_csv(StringIO(csv_data))
            with NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False)
                interpolator = read_file(tmp.name, header=True)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

        def test_valid_csv_without_header(self):
            csv_data = "1,4\n2,5\n3,6"
            df = pd.read_csv(StringIO(csv_data), header=None)
            with NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False, header=False)
                interpolator = read_file(tmp.name, header=False)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

        def test_invalid_csv_columns(self):
            csv_data = "a,b\n1,4\n2,5\n3,6"
            df = pd.read_csv(StringIO(csv_data))
            with NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df.to_csv(tmp.name, index=False)
                with pytest.raises(ValueError, match="Specified columns are not found in the file."):
                    read_file(tmp.name, x_col=2, y_col=3)

    class TestExcel:
        def test_valid_excel_with_header(self):
            df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
            with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                df.to_excel(tmp.name, index=False)
                interpolator = read_file(tmp.name, header=True)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

        def test_valid_excel_without_header(self):
            df = pd.DataFrame({0: [1, 2, 3], 1: [4, 5, 6]})
            with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                df.to_excel(tmp.name, index=False, header=False)
                interpolator = read_file(tmp.name, header=False)
                assert np.array_equal(interpolator.x, np.array([1, 2, 3]))
                assert np.array_equal(interpolator.y, np.array([4, 5, 6]))

        def test_invalid_excel_columns(self):
            df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
            with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                df.to_excel(tmp.name, index=False)
                with pytest.raises(ValueError, match="Specified columns are not found in the file."):
                    read_file(tmp.name, x_col=2, y_col=3)

    class TestInvalidFile:
        def test_invalid_file_type(self):
            with pytest.raises(ValueError, match="Unsupported file type. Must be a CSV or Excel file."):
                read_file('data.txt')

        def test_file_not_found(self):
            with pytest.raises(ValueError, match="Error reading file:"):
                read_file('non_existent_file.csv')


class TestInterpolate:
    def setup_method(self):
        self.x = np.array([0, 1, 2, 3])
        self.y = np.array([0, 10, 20, 30])
        self.new_x = 1.5

    def test_piecewise_linear(self):
        expected_y = np.interp(self.new_x, self.x, self.y)
        result_y = interpolate(self.x, self.y, self.new_x, 'PiecewiseLinear')
        assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

    def test_cubic_spline(self):
        interpolator = CubicSpline(self.x, self.y)
        expected_y = interpolator(self.new_x)
        result_y = interpolate(self.x, self.y, self.new_x, 'CubicSpline')
        assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

    def test_pchip(self):
        interpolator = PchipInterpolator(self.x, self.y)
        expected_y = interpolator(self.new_x)
        result_y = interpolate(self.x, self.y, self.new_x, 'Pchip')
        assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

    def test_akima1d(self):
        interpolator = Akima1DInterpolator(self.x, self.y)
        expected_y = interpolator(self.new_x)
        result_y = interpolate(self.x, self.y, self.new_x, 'Akima1D')
        assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

    def test_b_splines(self):
        interpolator = make_interp_spline(self.x, self.y)
        expected_y = interpolator(self.new_x)
        result_y = interpolate(self.x, self.y, self.new_x, 'B-splines')
        assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

    def test_invalid_method(self):
        with pytest.raises(ValueError, match="Invalid interpolation method"):
            interpolate(self.x, self.y, self.new_x, 'InvalidMethod')


class TestCleanArrays:
    def test_clean_arrays_no_invalid_values(self):
        # Test with no invalid values
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 4, 6, 8, 10])
        cleaned_x, cleaned_y = clean_arrays(x, y)
        assert np.array_equal(cleaned_x, x)
        assert np.array_equal(cleaned_y, y)

    def test_clean_arrays_with_zeros(self):
        # Test with zero values in y
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, 0, 6, 0, 10])
        with pytest.warns(UserWarning, match="Invalid values found in y"):
            cleaned_x, cleaned_y = clean_arrays(x, y)
        expected_x = np.array([1, 3, 5])
        expected_y = np.array([2, 6, 10])
        assert np.array_equal(cleaned_x, expected_x)
        assert np.array_equal(cleaned_y, expected_y)

    def test_clean_arrays_with_negative_values(self):
        # Test with negative values in y
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, -4, 6, -8, 10])
        with pytest.warns(UserWarning, match="Invalid values found in y"):
            cleaned_x, cleaned_y = clean_arrays(x, y)
        expected_x = np.array([1, 3, 5])
        expected_y = np.array([2, 6, 10])
        assert np.array_equal(cleaned_x, expected_x)
        assert np.array_equal(cleaned_y, expected_y)

    def test_clean_arrays_with_nan_values(self):
        # Test with NaN values in y
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, np.nan, 6, np.nan, 10])
        with pytest.warns(UserWarning, match="Invalid values found in y"):
            cleaned_x, cleaned_y = clean_arrays(x, y)
        expected_x = np.array([1, 3, 5])
        expected_y = np.array([2, 6, 10])
        assert np.array_equal(cleaned_x, expected_x)
        assert np.array_equal(cleaned_y, expected_y)

    def test_clean_arrays_with_inf_values(self):
        # Test with infinite values in y
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([2, np.inf, 6, -np.inf, 10])
        with pytest.warns(UserWarning, match="Invalid values found in y"):
            cleaned_x, cleaned_y = clean_arrays(x, y)
        expected_x = np.array([1, 3, 5])
        expected_y = np.array([2, 6, 10])
        assert np.array_equal(cleaned_x, expected_x)
        assert np.array_equal(cleaned_y, expected_y)

    def test_clean_arrays_all_invalid_values(self):
        # Test with all invalid values in y
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([0, -4, np.nan, np.inf, -np.inf])
        with pytest.warns(UserWarning, match="Invalid values found in y"):
            cleaned_x, cleaned_y = clean_arrays(x, y)
        assert cleaned_x.size == 0
        assert cleaned_y.size == 0
