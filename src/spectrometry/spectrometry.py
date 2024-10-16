from math import log, exp

from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator


class Spectrum:
    def __init__(self, energy, values):
        self.energy = energy  # Energy values
        self.values = values  # Corresponding values
        self.log_energy = None  # Log-transformed energy values
        self.log_values = None  # Log-transformed corresponding values

    def apply_log_transform(self):
        """Applies logarithmic transformation to the spectrum."""
        self.log_energy = [log(e) for e in self.energy]
        self.log_values = [log(v) for v in self.values]

    def interpolate(self, new_energies, log_scale=False, method='Akima1D'):
        """Interpolates the spectrum to a new set of energy values."""

        # Prepare interpolation input data in terms of the interpolation scale
        if log_scale:
            self.apply_log_transform()
            energies, values = self.log_energy, self.log_values
            new_energies = [log(e) for e in new_energies]
        else:
            energies, values = self.energy, self.values

        # Interpolate using one of the available methods. See
        # https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
        if method == 'CubicSpline':
            interpolator = CubicSpline(energies, values)
        elif method == 'PchipInterpolator':
            interpolator = PchipInterpolator(energies, values)
        elif method == 'Akima1D':
            interpolator = Akima1DInterpolator(energies, values)
        else:
            raise ValueError('Interpolation methods: CubicSpline, PchipInterpolator and Akima1D')
        interpolated_values = interpolator(new_energies)

        # Prepare interpolation output data in terms of the interpolation scale
        if log_scale:
            new_energies = [exp(e) for e in new_energies]
            interpolated_values = [exp(v) for v in interpolated_values]

        # Return spectrum
        return Spectrum(new_energies, interpolated_values)

    def calculate_hvl(self):
        """Calculates the Half-Value Layer (HVL) for the spectrum."""
        hvl = None
        return hvl
