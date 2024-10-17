from math import log

from spectrometry.spectrometry import Spectrum

print('Create a spectrum and check its linear and logarithmic representations')

# Input data
energies, fluences = [1, 2, 3], [10, 20, 30]
print(f'Input data: {energies}, {fluences}')

# Create Spectrum object
spectrum = Spectrum(energies, fluences)
print(f'Spectrum (lin scale): {spectrum.energy}, {spectrum.values}')

# Apply logarithmic transformation
spectrum.apply_log_transform()
print(f'Spectrum (log scale): {spectrum.log_energy}, {spectrum.log_values}')
print(f'Spectrum (log scale): {[log(i) for i in energies]}, {[log(i) for i in fluences]}')

print()
print('Interpolate a spectrum using linear or logarithmic interpolation')

# Interpolate in linear scale
interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=False)
print(f'Linear interpolation: {interpolated_spectrum.energy}, {interpolated_spectrum.values}')

# Interpolate in logarithmic scale
interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True)
print(f'Logarithmic interpolation): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')

print()
print('Interpolate a spectrum using different interpolation methods')

# Interpolate in logarithmic scale using CubicSplines
interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='CubicSpline')
print(f'CubicSplines: {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
# Interpolate in logarithmic scale using PchipInterpolator
interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='PchipInterpolator')
print(f'PchipInterpolator: {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
# Interpolate in logarithmic scale using Akima1D
interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='Akima1D')
print(f'Akima1D: {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
