from io import StringIO
from tempfile import NamedTemporaryFile

import numpy as np
import pandas as pd
import pytest
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator, make_interp_spline

from src.spectrometry.interpolator import Interpolator, read_file


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

    class TestInterpolate:
        def setup_method(self):
            self.x = np.array([0, 1, 2, 3])
            self.y = np.array([0, 10, 20, 30])
            self.new_x = 1.5
            self.interpolator = Interpolator(x=self.x, y=self.y)

        def test_piecewise_linear(self):
            expected_y = np.interp(self.new_x, self.x, self.y)
            result_y = self.interpolator.interpolate(self.new_x, method='PiecewiseLinear')
            assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

        def test_cubic_spline(self):
            interpolator = CubicSpline(self.x, self.y)
            expected_y = interpolator(self.new_x)
            result_y = self.interpolator.interpolate(self.new_x, method='CubicSpline')
            assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

        def test_pchip(self):
            interpolator = PchipInterpolator(self.x, self.y)
            expected_y = interpolator(self.new_x)
            result_y = self.interpolator.interpolate(self.new_x, method='Pchip')
            assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

        def test_akima1d(self):
            interpolator = Akima1DInterpolator(self.x, self.y)
            expected_y = interpolator(self.new_x)
            result_y = self.interpolator.interpolate(self.new_x, method='Akima1D')
            assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

        def test_b_splines(self):
            interpolator = make_interp_spline(self.x, self.y)
            expected_y = interpolator(self.new_x)
            result_y = self.interpolator.interpolate(self.new_x, method='B-splines')
            assert result_y == expected_y, f"Expected {expected_y}, but got {result_y}"

        def test_invalid_method(self):
            with pytest.raises(ValueError, match="Interpolation methods: PiecewiseLinear, CubicSpline, Pchip, Akima1D, B-splines"):
                self.interpolator.interpolate(self.new_x, method='InvalidMethod')


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
