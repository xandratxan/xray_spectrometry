import warnings

import numpy as np

# x_new = [1.5, 2.5]
#
# print('PiecewiseLinear')
#
# print('Valid')
# data_valid = read_file("../data/log_scale/valid.csv")
# y_new_valid = data_valid(x_new, 'PiecewiseLinear', log=True)
# print(y_new_valid)
# # [15. 25.]
#
# print('Zero')
# data_zero = read_file("../data/log_scale/zero.csv")
# y_new_zero = data_zero(x_new, 'PiecewiseLinear', log=True)
# print(y_new_zero)
# # RuntimeWarning: divide by zero encountered in log self.log_y = np.log(self.y)
# # [15.  0.]
# # if log, check for zeros and remove
#
# print('Negative')
# data_negative = read_file("../data/log_scale/negative.csv")
# y_new_negative = data_negative(x_new, 'PiecewiseLinear', log=True)
# print(y_new_negative)
# # RuntimeWarning: invalid value encountered in log self.log_y = np.log(self.y)
# # [15. nan]
# # if log, check for negative numbers and remove
#
# print('String')
# try:
#     data_str = read_file("../data/log_scale/str.csv")
# except ValueError as e:
#     print(e)
# # ValueError: Error reading file: Interpolator constructor failed. Elements of arguments must be numerical.
#
# print('None')
# data_none = read_file("../data/log_scale/none.csv")
# # None is read as np.nan
# y_new_none = data_none(x_new, 'PiecewiseLinear', log=True)
# print(y_new_none)
# # [15. nan]
# # if log, check for numpy nan and remove
#
# print('Gap')
# data_gap = read_file("../data/log_scale/gap.csv")
# # None is read as np.nan
# y_new_gap = data_gap(x_new, 'PiecewiseLinear', log=True)
# print(y_new_gap)
# # if log, check for numpy nan and remove
#
# print('CubicSpline, Pchip, Akima1D')
#
# print('Valid')
# data_valid = read_file("../data/log_scale/valid.csv")
# y_new_valid = data_valid(x_new, 'CubicSpline', log=True)
# print(y_new_valid)
# # [15. 25.]
#
# print('Zero')
# data_zero = read_file("../data/log_scale/zero.csv")
# y_new_zero = data_zero(x_new, 'CubicSpline', log=True)
# print(y_new_zero)
# # ValueError: `y` must contain only finite values.
#
# print('Negative')
# data_negative = read_file("../data/log_scale/negative.csv")
# y_new_negative = data_negative(x_new, 'CubicSpline', log=True)
# print(y_new_negative)
# # ValueError: `y` must contain only finite values.
#
# print('None')
# data_none = read_file("../data/log_scale/none.csv")
# # None is read as np.nan
# y_new_none = data_none(x_new, 'CubicSpline', log=True)
# print(y_new_none)
# # ValueError: `y` must contain only finite values.
#
# print('Gap')
# data_gap = read_file("../data/log_scale/gap.csv")
# # None is read as np.nan
# y_new_gap = data_gap(x_new, 'CubicSpline', log=True)
# print(y_new_gap)
# # # ValueError: `y` must contain only finite values.
#
# print('B-splines')
#
# print('Valid')
# data_valid = read_file("../data/log_scale/valid.csv")
# y_new_valid = data_valid(x_new, 'B-splines', log=True)
# print(y_new_valid)
# # [15. 25.]
#
# print('Zero')
# data_zero = read_file("../data/log_scale/zero.csv")
# y_new_zero = data_zero(x_new, 'B-splines', log=True)
# print(y_new_zero)
# # ValueError: Array must not contain infs or nans.
#
# print('Negative')
# data_negative = read_file("../data/log_scale/negative.csv")
# y_new_negative = data_negative(x_new, 'B-splines', log=True)
# print(y_new_negative)
# # ValueError: Array must not contain infs or nans.
#
# print('None')
# data_none = read_file("../data/log_scale/none.csv")
# # None is read as np.nan
# y_new_none = data_none(x_new, 'B-splines', log=True)
# print(y_new_none)
# # ValueError: Array must not contain infs or nans.
#
# print('Gap')
# data_gap = read_file("../data/log_scale/gap.csv")
# # None is read as np.nan
# y_new_gap = data_gap(x_new, 'B-splines', log=True)
# print(y_new_gap)
# # ValueError: Array must not contain infs or nans.



def clean_arrays(x, y):

    y = np.array(y).astype(np.float64)

    # Check for invalid values in y
    invalid_mask = (y == 0) | (y < 0) | np.isnan(y) | np.isinf(y)

    # If there are any invalid values, raise a warning
    if np.any(invalid_mask):
        warnings.warn("Invalid values found in y. Corresponding elements in x and y will be deleted.")

        # Remove invalid elements from x and y
        x = x[~invalid_mask]
        y = y[~invalid_mask]
    else:
        print('no invalid elements')

    return x, y


# Example usage
x_ = np.array([ 1,  2,  3,  4,  5,  6,  7,  8,  9])
y_ = np.array([10,  0, 30,  -40,  50,  np.nan,  70,  None,  90])

cleaned_x, cleaned_y = clean_arrays(x_, y_)
print("Cleaned x:", cleaned_x)
print("Cleaned y:", cleaned_y)

# Example usage
x_ = np.array([ 1,  2,  3,  4,  5,  6,  7,  8,  9])
y_ = np.array([10,  20, 30,  40,  50,  60,  70,  80,  90])

cleaned_x, cleaned_y = clean_arrays(x_, y_)
print("Cleaned x:", cleaned_x)
print("Cleaned y:", cleaned_y)
