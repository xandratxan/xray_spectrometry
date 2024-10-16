import math
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator


class Spectrum:
    def __init__(self, energy, values):
        self.energy = energy  # Energy values
        self.values = values  # Corresponding values
        self.log_energy = None  # Log-transformed energy values
        self.log_values = None  # Log-transformed corresponding values

    def apply_log_transform(self):
        """Applies logarithmic transformation to the spectrum."""
        self.log_energy = [math.log(e) for e in self.energy]
        self.log_values = [math.log(v) for v in self.values]

    def interpolate(self, new_energies, log_scale=False, method='Akima1D'):
        """Interpolates the spectrum to a new set of energy values."""
        if log_scale:
            # Case 2: interpolate using log scale for the spectrum and new energies using akima
            self.apply_log_transform()
            log_new_energies = [math.log(e) for e in new_energies]

            # https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
            if method=='CubicSpline':
                interpolator = CubicSpline(self.log_energy, self.log_values)
            elif method=='PchipInterpolator':
                interpolator = PchipInterpolator(self.log_energy, self.log_values)
            elif method=='Akima1D':
                interpolator = Akima1DInterpolator(self.log_energy, self.log_values)
            else:
                raise ValueError('Interpolation methods: CubicSpline, PchipInterpolator and Akima1D')

            log_interpolated_values = interpolator(log_new_energies)

            interpolated_values = [math.exp(v) for v in log_interpolated_values]
        else:
            # Case 1: interpolate using linear scale for the spectrum and new energies using akima
            # https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
            if method == 'CubicSpline':
                interpolator = CubicSpline(self.energy, self.values)
            elif method == 'PchipInterpolator':
                interpolator = PchipInterpolator(self.energy, self.values)
            elif method == 'Akima1D':
                interpolator = Akima1DInterpolator(self.energy, self.values)
            else:
                raise ValueError('Interpolation methods: PchipInterpolator CubicSpline, and Akima1D')

            interpolated_values = interpolator(new_energies)

        return Spectrum(new_energies, interpolated_values)

    def calculate_hvl(self):
        """Calculates the Half-Value Layer (HVL) for the spectrum."""
        hvl = None
        return hvl


def main():
    # Input data
    energies, fluences = [1, 2, 3], [10, 20, 30]
    print(f'Input data: {energies}, {fluences}')

    # Create Spectrum object
    spectrum = Spectrum(energies, fluences)
    print(f'Spectrum (lin scale): {spectrum.energy}, {spectrum.values}')

    # Apply logarithmic transformation
    spectrum.apply_log_transform()
    print(f'Spectrum (log scale): {spectrum.log_energy}, {spectrum.log_values}')
    print(f'Spectrum (log scale): {[math.log(i) for i in energies]}, {[math.log(i) for i in fluences]}')

    # Interpolate in linear scale
    interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=False)
    print(f'Interpolated spectrum (lin interpolation): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
    # Interpolate in logarithmic scale
    interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True)
    print(f'Interpolated spectrum (log interpolation): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')

    # Interpolate in logarithmic scale using CubicSplines
    interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='CubicSpline')
    print(f'Interpolated spectrum (CubicSplines): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
    # Interpolate in logarithmic scale using PchipInterpolator
    interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='PchipInterpolator')
    print(f'Interpolated spectrum (PchipInterpolator): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')
    # Interpolate in logarithmic scale using Akima1D
    interpolated_spectrum = spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True, method='Akima1D')
    print(f'Interpolated spectrum (Akima1D): {interpolated_spectrum.energy}, {interpolated_spectrum.values}')


if __name__ == "__main__":
    main()
