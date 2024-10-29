from spectrometry import read_file

# From CSV without header
interpolator1 = read_file("../data/read_file/data_no_header.csv", sheet_name=0, x_col=0, y_col=1, header=False)
# From CSV with header
interpolator2 = read_file("../data/read_file/data_header.csv", sheet_name=0, x_col=0, y_col=1, header=True)
# From Excel without header
interpolator3 = read_file("../data/read_file/data_no_header.xlsx", sheet_name=0, x_col=0, y_col=1, header=False)
# From Excel with header
interpolator4 = read_file("../data/read_file/data_header.xlsx", sheet_name=0, x_col=0, y_col=1, header=True)
# Invalid file
try:
    interpolator5 = read_file("../data/read_file/dummy.txt")
except ValueError as e:
    print(e)
try:
    interpolator6 = read_file("../data/read_file/corrupted.csv")
except ValueError as e:
    print(e)
