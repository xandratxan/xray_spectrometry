import math
from scipy.interpolate import Akima1DInterpolator


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

    def interpolate(self, new_energies, log_scale=False):
        """Interpolates the spectrum to a new set of energy values."""
        if log_scale:
            # Case 2: interpolate using log scale for the spectrum and new energies using akima
            self.apply_log_transform()
            log_new_energies = [math.log(e) for e in new_energies]
            interpolator = Akima1DInterpolator(self.log_energy, self.log_values)
            log_interpolated_values = interpolator(log_new_energies)
            interpolated_values = [math.exp(v) for v in log_interpolated_values]
        else:
            # Case 1: interpolate using linear scale for the spectrum and new energies using akima
            interpolator = Akima1DInterpolator(self.energy, self.values)
            interpolated_values = interpolator(new_energies)

        return Spectrum(new_energies, interpolated_values)

    def calculate_hvl(self):
        """Calculates the Half-Value Layer (HVL) for the spectrum."""
        hvl = None
        return hvl


def main():
    # Input data
    fluence_energies, fluence_values = [1, 2, 3], [10, 20, 30]
    print(f'Fluence input data: {fluence_energies}, {fluence_values}')

    # Create Spectrum object
    fluence_spectrum = Spectrum(fluence_energies, fluence_values)
    print(f'Fluence spectrum (lin scale): {fluence_spectrum.energy}, {fluence_spectrum.values}')

    # Apply logarithmic transformation
    fluence_spectrum.apply_log_transform()
    print(f'Fluence spectrum (log scale): {fluence_spectrum.log_energy}, {fluence_spectrum.log_values}')
    print(f'Fluence spectrum (log scale): {[math.log(i) for i in fluence_energies]}, {[math.log(i) for i in fluence_values]}')

    interpolated_fluence_spectrum = fluence_spectrum.interpolate([1, 1.5, 2, 2.5, 3])
    print(f'Interpolated fluence spectrum (lin interpolation): {interpolated_fluence_spectrum.energy}, {interpolated_fluence_spectrum.values}')

    interpolated_fluence_spectrum = fluence_spectrum.interpolate([1, 1.5, 2, 2.5, 3], log_scale=True)
    print(f'Interpolated fluence spectrum (log interpolation): {interpolated_fluence_spectrum.energy}, {interpolated_fluence_spectrum.values}')

if __name__ == "__main__":
    main()
