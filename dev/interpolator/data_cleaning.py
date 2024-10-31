from spectrometry.interpolator import read_file

x_new = [1.5, 2.5]

print('PiecewiseLinear')

print('Valid')
data_valid = read_file("../data/log_scale/valid.csv")
y_new_valid = data_valid(x_new, 'PiecewiseLinear', log=True)
print(y_new_valid)
# [15. 25.]

print('Zero')
data_zero = read_file("../data/log_scale/zero.csv")
y_new_zero = data_zero(x_new, 'PiecewiseLinear', log=True)
print(y_new_zero)

print('Negative')
data_negative = read_file("../data/log_scale/negative.csv")
y_new_negative = data_negative(x_new, 'PiecewiseLinear', log=True)
print(y_new_negative)

print('String')
try:
    data_str = read_file("../data/log_scale/str.csv")
except ValueError as e:
    print(e)

print('None')
data_none = read_file("../data/log_scale/none.csv")
y_new_none = data_none(x_new, 'PiecewiseLinear', log=True)
print(y_new_none)

print('Gap')
data_gap = read_file("../data/log_scale/gap.csv")
y_new_gap = data_gap(x_new, 'PiecewiseLinear', log=True)
print(y_new_gap)

print('CubicSpline, Pchip, Akima1D')

print('Valid')
data_valid = read_file("../data/log_scale/valid.csv")
y_new_valid = data_valid(x_new, 'CubicSpline', log=True)
print(y_new_valid)

print('Zero')
data_zero = read_file("../data/log_scale/zero.csv")
y_new_zero = data_zero(x_new, 'CubicSpline', log=True)
print(y_new_zero)

print('Negative')
data_negative = read_file("../data/log_scale/negative.csv")
y_new_negative = data_negative(x_new, 'CubicSpline', log=True)
print(y_new_negative)

print('None')
data_none = read_file("../data/log_scale/none.csv")
y_new_none = data_none(x_new, 'CubicSpline', log=True)
print(y_new_none)

print('Gap')
data_gap = read_file("../data/log_scale/gap.csv")
y_new_gap = data_gap(x_new, 'CubicSpline', log=True)
print(y_new_gap)

print('B-splines')

print('Valid')
data_valid = read_file("../data/log_scale/valid.csv")
y_new_valid = data_valid(x_new, 'B-splines', log=True)
print(y_new_valid)
# [15. 25.]

print('Zero')
data_zero = read_file("../data/log_scale/zero.csv")
y_new_zero = data_zero(x_new, 'B-splines', log=True)
print(y_new_zero)
# ValueError: Array must not contain infs or nans.

print('Negative')
data_negative = read_file("../data/log_scale/negative.csv")
y_new_negative = data_negative(x_new, 'B-splines', log=True)
print(y_new_negative)
# ValueError: Array must not contain infs or nans.

print('None')
data_none = read_file("../data/log_scale/none.csv")
# None is read as np.nan
y_new_none = data_none(x_new, 'B-splines', log=True)
print(y_new_none)
# ValueError: Array must not contain infs or nans.

print('Gap')
data_gap = read_file("../data/log_scale/gap.csv")
# None is read as np.nan
y_new_gap = data_gap(x_new, 'B-splines', log=True)
print(y_new_gap)
# ValueError: Array must not contain infs or nans.
