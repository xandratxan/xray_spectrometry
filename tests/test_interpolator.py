import numpy as np
import pandas as pd
import pytest

from spectrometry import Interpolator


class TestInterpolator:
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

# TODO: code coverage report
