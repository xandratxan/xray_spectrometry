# xray_spectrometry
Tools for experimental spectrometry in an X-ray metrology laboratory

## Development notes
PAL provides the next reference files:
- Script to calculate HVL from experimental spectra.
- Script to calculate hK from experimental spectra.
- CSV files for x ray spectra for various x ray qualities.

The goal the is to develope a tool with the next characteristics:
- Read an x ray spectrum form CSV file.
- Compute HVL or hk from the x ray spectrum.

## Script to calculate HVL from experimental spectra

### What is the goal of this code?

The goal of this code is to calculate the Half-Value Layer (HVL) for a material based on experimental data. 
The HVL is a measure of how much material is needed to reduce the intensity of radiation by half. 
Here’s a simplified breakdown:

1. **Read Data**: The code reads data from several files that contain information about how radiation interacts with a material (like aluminum).
This data includes:
- *mutr/rho* (mass energy-transfer coefficient) vs. energy.
- *mu/rho* (mass attenuation coefficient) vs. energy.
- *Fluence* (the flow of radiation) vs. energy.
2. **Logarithmic Conversion**: It converts the energy and coefficient values to their logarithmic forms. 
This helps in the interpolation process.
3. **Interpolation**: The code uses a mathematical technique called Akima interpolation to create smooth curves from the data points.
This allows it to estimate values between the known data points.
4. **Calculate HVL**: It then uses these interpolated values to calculate how much material (in this case, aluminum) is needed to reduce the radiation intensity by half.
This is done through an iterative process where it adjusts the thickness of the material until the desired reduction in radiation is achieved.
5. **Output**: Finally, it prints out the calculated HVL value.

In essence, the code is designed to determine the thickness of a material required to halve the intensity of radiation passing through it, using experimental data and mathematical interpolation.

### What the script does step by step?

Let’s go through this code step by step:

```python
###########################################################
# Script to calculate HVL from experimental spectra
###########################################################

# Import necessary libraries
import pandas as pd  # Import pandas for data handling (not used in the script)
import math  # Import math for mathematical operations
from scipy.interpolate import Akima1DInterpolator  # Import Akima1DInterpolator for interpolation
```

1. **Imports and Setup**:
- ``import pandas as pd``, ``import math``, and ``from scipy.interpolate import Akima1DInterpolator``: Import necessary libraries for data handling, mathematical operations, and interpolation.

```python
# Section 1: Read mutr/rho vs E data
logEmutr = []  # Initialize list to store log of energy values for mutr/rho
logmutr = []  # Initialize list to store log of mutr/rho values
archivo_mutr = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\mutr.txt"
with open(archivo_mutr, 'r') as f:  # Open the mutr/rho file
    for linea in f:  # Read each line in the file
        col1 = linea.strip().replace('\t', ' ').split()  # Extract the first column (energy)
        col2 = linea.strip().replace('\t', ' ').split()  # Extract the second column (mutr/rho)
        try:
            numeroE = float(col1)  # Convert energy to float
            lnEmutr = math.log(numeroE)  # Take the logarithm of energy
            logEmutr.append(lnEmutr)  # Append log energy to list
            numeromutr = float(col2)  # Convert mutr/rho to float
            lnmutr = math.log(numeromutr)  # Take the logarithm of mutr/rho
            logmutr.append(lnmutr)  # Append log mutr/rho to list
        except ValueError as e:  # Handle conversion errors
            print(f'Error: No se puede convertir este valor a float1: {linea}')
            continue
```

2. **Reading mutr/rho Data**:
- Initialize empty lists logEmutr and logmutr.
- Open the file mutr.txt and read each line.
- Split each line into two columns, convert them to floats, and take their logarithms.
- Append the logarithmic values to logEmutr and logmutr.

```python
# Section 2: Read mu/rho vs E data
logEmu = []  # Initialize list to store log of energy values for mu/rho
logmu = []  # Initialize list to store log of mu/rho values
densityAl = 2.699  # Density of aluminum
archivo_muAl = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\muAl.txt"
with open(archivo_muAl, 'r') as f:  # Open the mu/rho file
    for linea in f:  # Read each line in the file
        col1 = linea.strip().replace('\t', ' ').split()  # Extract the first column (energy)
        col2 = linea.strip().replace('\t', ' ').split()  # Extract the second column (mu/rho)
        try:
            numeroEmu = float(col1)  # Convert energy to float
            lnEmu = math.log(numeroEmu)  # Take the logarithm of energy
            logEmu.append(lnEmu)  # Append log energy to list
            numeromu = float(col2)  # Convert mu/rho to float
            numeromu = numeromu * densityAl  # Adjust mu/rho by the density of aluminum
            lnmu = math.log(numeromu)  # Take the logarithm of adjusted mu/rho
            logmu.append(lnmu)  # Append log mu/rho to list
        except ValueError as e:  # Handle conversion errors
            print(f'Error: No se puede convertir este valor a float2: {linea}')
            continue
```

3. **Reading mu/rho Data**:
- Initialize empty lists logEmu and logmu.
- Set the density of aluminum (densityAl = 2.699).
- Open the file muAl.txt and read each line.
- Split each line into two columns, convert them to floats, multiply the second column by the density, and take their logarithms.
- Append the logarithmic values to logEmu and logmu.

```python
# Section 3: Read fluence vs E data
E = []  # Initialize list to store energy values
logE = []  # Initialize list to store log of energy values
fluence = []  # Initialize list to store fluence values
archivo_fluence = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_qualities_IR14D_2022\spec30.txt"

with open(archivo_fluence, 'r') as f:  # Open the fluence file
    for linea in f:  # Read each line in the file
        col1 = linea.strip().replace('\t', ' ').split()  # Extract the first column (energy)
        col2 = linea.strip().replace('\t', ' ').split()  # Extract the second column (fluence)
        numeroE = float(col1)  # Convert energy to float
        E_ln = math.log(numeroE)  # Take the logarithm of energy
        E.append(numeroE)  # Append energy to list
        logE.append(E_ln)  # Append log energy to list
        numeroflu = float(col2)  # Convert fluence to float
        fluence.append(numeroflu)  # Append fluence to list
```

4. **Reading Fluence Data**:
- Initialize empty lists E, logE, and fluence.
- Open the file spec30.txt and read each line.
- Split each line into two columns, convert them to floats, and take the logarithm of the first column.
- Append the values to E, logE, and fluence.

```python
# Section 4: Interpolation of mutr/rho and mu
interpolacion_Lnmu = Akima1DInterpolator(logEmu, logmu, axis=0)  # Create interpolator for mu/rho
interpolacion_Lnmutr = Akima1DInterpolator(logEmutr, logmutr, axis=0)  # Create interpolator for mutr/rho
mu = []  # Initialize list to store interpolated mu values
mutr = []  # Initialize list to store interpolated mutr values
for i in logE:  # For each log energy value
    try:
        interp_Lnmu = interpolacion_Lnmu(i)  # Interpolate log mu value
        interp_Lnmutr = interpolacion_Lnmutr(i)  # Interpolate log mutr value
        mu_int = math.exp(interp_Lnmu)  # Convert interpolated log mu back to original scale
        mutr_int = math.exp(interp_Lnmutr)  # Convert interpolated log mutr back to original scale
        mu.append(mu_int)  # Append interpolated mu to list
        mutr.append(mutr_int)  # Append interpolated mutr to list
    except ValueError:  # Handle interpolation errors
        mu_int.append(float('nan'))
```

5. **Interpolation**:
- Create interpolators interpolacion_Lnmu and interpolacion_Lnmutr using Akima1DInterpolator.
- Initialize empty lists mu and mutr.
- For each value in logE, interpolate the logarithmic values and convert them back to the original scale using math.exp.

```python
# Section 5: HVL Calculation
testq = 20.0  # Initial guess for HVL
delta = testq  # Initial step size
ratio = 0.5  # Desired transmission ratio

while delta > 0.000001:  # Continue until the step size is very small
    delta = delta * 0.5  # Halve the step size
    suma_Katt = 0  # Initialize sum for attenuated kerma
    suma_K0 = 0  # Initialize sum for non-attenuated kerma
    for i in range(len(E)):  # For each energy value
        attenuation = math.exp(-mu[i] * testq)  # Calculate attenuation factor
        Katt = E[i] * fluence[i] * mutr[i] * attenuation  # Calculate attenuated kerma
        suma_Katt = suma_Katt + Katt  # Sum attenuated kerma
        K0 = E[i] * fluence[i] * mutr[i]  # Calculate non-attenuated kerma
        suma_K0 = suma_K0 + K0  # Sum non-attenuated kerma

    trans = suma_Katt / suma_K0  # Calculate transmission ratio

    if abs(trans - ratio) < 0.000005:  # Check if transmission ratio is close to desired value
        HVL = testq  # Set HVL to current guess
        break  # Exit the loop
    if trans > ratio:  # If transmission is too high
        testq = testq + delta  # Increase the guess
    else:  # If transmission is too low
        testq = testq - delta  # Decrease the guess

print(f'HVL is equal to:  {HVL}')  # Print the calculated HVL
```

6. **HVL Calculation**:
- Initialize testq to 20.0 and delta to testq.
- Set the target transmission ratio to 0.5.
- Use a while loop to iteratively adjust testq until the calculated transmission ratio is close to 0.5.
- In each iteration, calculate the attenuated and non-attenuated kerma sums (suma_Katt and suma_K0).
- Calculate the transmission ratio and adjust testq accordingly.
- Break the loop when the transmission ratio is sufficiently close to 0.5.
- Print the calculated HVL value.

This script essentially reads experimental data, interpolates necessary coefficients, and calculates the Half-Value Layer (HVL) for a given material based on the provided spectra.

### Simplifying the script using Python functions

Simplifying the script using Python functions can make it more modular, readable, and easier to maintain. 

Here’s a refactored version of the script with functions:

```python
import pandas as pd  # Import pandas for data handling (not used in the script)
import math  # Import math for mathematical operations
from scipy.interpolate import Akima1DInterpolator  # Import Akima1DInterpolator for interpolation

def read_data(file_path):
    """Reads data from a file and returns the raw values."""
    E = []
    values = []
    with open(file_path, 'r') as f:
        for line in f:
            col1, col2 = line.strip().replace('\t', ' ').split()[:2]
            try:
                E.append(float(col1))
                values.append(float(col2))
            except ValueError:
                print(f'Error: Cannot convert value to float: {line}')
                continue
    return E, values

def transform_to_log(E, values, density=None):
    """Transforms energy and values to their logarithmic forms."""
    logE = []
    log_values = []
    for i in range(len(E)):
        try:
            logE.append(math.log(E[i]))
            value = values[i]
            if density:
                value *= density
            log_values.append(math.log(value))
        except ValueError:
            print(f'Error: Cannot convert value to log: E={E[i]}, value={values[i]}')
            continue
    return logE, log_values

def interpolate_data(logE, log_values):
    """Interpolates data using Akima1DInterpolator."""
    return Akima1DInterpolator(logE, log_values, axis=0)

def calculate_hvl(E, logE, fluence, mu, mutr, ratio=0.5):
    """Calculates the Half-Value Layer (HVL)."""
    testq = 20.0
    delta = testq
    while delta > 0.000001:
        delta *= 0.5
        suma_Katt = suma_K0 = 0
        for i in range(len(E)):
            attenuation = math.exp(-mu[i] * testq)
            Katt = E[i] * fluence[i] * mutr[i] * attenuation
            suma_Katt += Katt
            K0 = E[i] * fluence[i] * mutr[i]
            suma_K0 += K0
        trans = suma_Katt / suma_K0
        if abs(trans - ratio) < 0.000005:
            return testq
        if trans > ratio:
            testq += delta
        else:
            testq -= delta
    return testq

def main():
    # File paths
    archivo_mutr = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\mutr.txt"
    archivo_muAl = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\muAl.txt"
    archivo_fluence = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_qualities_IR14D_2022\spec30.txt"

    # Read data
    E_mutr, mutr_values = read_data(archivo_mutr)
    E_mu, mu_values = read_data(archivo_muAl)
    E_fluence, fluence = read_data(archivo_fluence)

    # Transform data to logarithmic values
    logEmutr, logmutr = transform_to_log(E_mutr, mutr_values)
    logEmu, logmu = transform_to_log(E_mu, mu_values, density=2.699)
    logE, _ = transform_to_log(E_fluence, E_fluence)  # Only need logE for fluence

    # Interpolate data
    interpolacion_Lnmu = interpolate_data(logEmu, logmu)
    interpolacion_Lnmutr = interpolate_data(logEmutr, logmutr)

    # Interpolate mu and mutr values
    mu = [math.exp(interpolacion_Lnmu(i)) for i in logE]
    mutr = [math.exp(interpolacion_Lnmutr(i)) for i in logE]

    # Calculate HVL
    HVL = calculate_hvl(E_fluence, logE, fluence, mu, mutr)
    print(f'HVL is equal to: {HVL}')

if __name__ == "__main__":
    main()
```

Here’s a brief explanation of how the new code works:

1. **Reading data**: The ``read_data`` function reads raw energy and value data from a file.
2. **Logarithmic transformation**: The ``transform_to_log`` function converts these raw values to their logarithmic forms, optionally adjusting values by a given density.
3. **Interpolation**: The ``interpolate_data`` function uses Akima1DInterpolator to create smooth curves from the log-transformed data, allowing for estimation of values between known data points.
4. **HVL Calculation**: The ``calculate_hvl`` function iteratively adjusts the thickness of the material (HVL) until the calculated transmission ratio of radiation is close to the desired value (0.5).
5. **Main Function**: The ``main`` function coordinates the entire process:
- It reads the data from files.
- Transforms the data to logarithmic values.
- Interpolates the data.
- Calculates the HVL.
- Prints the final HVL value.

This modular approach makes the code more organized, easier to understand, and maintain. 
Each function has a clear responsibility, improving readability and reusability.

### Restructuring the code using OOP

Refactoring to OOP can significantly improve the structure and maintainability of your code.
Here we have a collection of energy values and their corresponding measurements. 
Instead of handling these values with separate functions and variables, 
we can create a blueprint (a class) that represents a spectrum. 
This blueprint will define what a spectrum is and what it can do.

Here's how we can model a spectrum using OOP:

1. **Create a Blueprint (Class)**:
- We’ll create a class called ``Spectrum``. This class will act as a blueprint for any spectrum we want to work with.
2. **Define Attributes (Data)**:
- The class will have attributes to store the energy values (``E``) and their corresponding measurements ('values').
3. **Add Methods (Behaviors)**:
- **Logarithmic Transformation**: A method to convert the energy values and measurements to their logarithmic forms.
- **Interpolation**: A method to estimate values at new energy points using the existing data.
- **HVL Calculation**: A method to calculate the Half-Value Layer (HVL), which tells us how much material is needed to reduce the radiation intensity by half.

In this way, when you create a Spectrum object, you can easily perform operations like transforming the data, interpolating new values, and calculating the HVL, all within the same object.

Here’s a refactored version of the script using OOP:

```python
import math
from scipy.interpolate import Akima1DInterpolator

class Spectrum:
    def __init__(self, E, values):
        self.E = E  # Energy values
        self.values = values  # Corresponding values
        self.logE = None  # Log-transformed energy values
        self.log_values = None  # Log-transformed corresponding values

    def apply_log_transform(self):
        """Applies logarithmic transformation to the spectrum."""
        self.logE = [math.log(e) for e in self.E]
        self.log_values = [math.log(v) for v in self.values]

    def interpolate(self, new_E):
        """Interpolates the spectrum to a new set of energy values."""
        if self.logE is None or self.log_values is None:
            raise ValueError("Logarithmic transformation must be applied before interpolation.")
        
        interpolator = Akima1DInterpolator(self.logE, self.log_values)
        log_new_E = [math.log(e) for e in new_E]
        interpolated_log_values = interpolator(log_new_E)
        interpolated_values = [math.exp(v) for v in interpolated_log_values]
        return interpolated_values

    def calculate_hvl(self, fluence, mu, mutr, ratio=0.5):
        """Calculates the Half-Value Layer (HVL) for the spectrum."""
        testq = 20.0
        delta = testq
        while delta > 0.000001:
            delta *= 0.5
            suma_Katt = suma_K0 = 0
            for i in range(len(self.E)):
                attenuation = math.exp(-mu[i] * testq)
                Katt = self.E[i] * fluence[i] * mutr[i] * attenuation
                suma_Katt += Katt
                K0 = self.E[i] * fluence[i] * mutr[i]
                suma_K0 += K0
            trans = suma_Katt / suma_K0
            if abs(trans - ratio) < 0.000005:
                return testq
            if trans > ratio:
                testq += delta
            else:
                testq -= delta
        return testq

# Example usage
def main():
    # Example data
    E = [10, 20, 30, 40, 50]  # Energy values
    values = [1, 2, 3, 4, 5]  # Corresponding values
    fluence = [0.1, 0.2, 0.3, 0.4, 0.5]  # Example fluence values
    mu = [0.01, 0.02, 0.03, 0.04, 0.05]  # Example mu values
    mutr = [0.001, 0.002, 0.003, 0.004, 0.005]  # Example mutr values

    # Create Spectrum object
    spectrum = Spectrum(E, values)

    # Apply logarithmic transformation
    spectrum.apply_log_transform()

    # Interpolate to new energy values
    new_E = [15, 25, 35, 45]  # New energy values for interpolation
    interpolated_values = spectrum.interpolate(new_E)
    print(f'Interpolated values: {interpolated_values}')

    # Calculate HVL
    HVL = spectrum.calculate_hvl(fluence, mu, mutr)
    print(f'HVL is equal to: {HVL}')

if __name__ == "__main__":
    main()
```

Explanation:

1. **Class Definition**:
- ``Spectrum``: A class to handle energy values and corresponding values.
2. **Attributes**:
- ``E``: List of energy values.
- ``values``: List of corresponding values.
- ``logE``: List of logarithmic energy values (initialized as None).
- ``log_values``: List of logarithmic corresponding values (initialized as None).
3. **Methods**:
- ``apply_log_transform()``: Applies logarithmic transformation to E and values.
- ``interpolate(new_E)``: Interpolates the spectrum to a new set of energy values (new_E).
- ``calculate_hvl(fluence, mu, mutr, ratio=0.5)``: Calculates the Half-Value Layer (HVL) for the spectrum.

Example Usage:

The main function demonstrates how to create a Spectrum object, apply logarithmic transformation, interpolate to new energy values, and calculate the HVL.

This approach encapsulates the functionality within a single class, making the code more modular and easier to manage. If you have any questions or need further adjustments, feel free to ask!

## How SpekPy computes HVL

Here's how SpekPy computes the HVL for a simulated spectrum (see this [example script](https://bitbucket.org/spekpy/spekpy_release/src/master/examples/generate_spectrum_and_use_all_get_methods.py):

```python
import spekpy as sp
# Generate unfiltered spectrum
s = sp.Spek(kvp=120, th=12)
# Filter the spectrum
s.multi_filter([['Al', 4.0], ['Air', 1000]])
# Compute first and secon HVL for Al and Cu
print('1st Hvl:', s.get_hvl1(), 'mmAl')
print('2nd Hvl:', s.get_hvl2(), 'mmAl')
print('1st Hvl:', s.get_hvl1(matl='Cu'), 'mmCu')
print('2nd Hvl:', s.get_hvl2(matl='Cu'), 'mmCu')
```

Let's take the ``get_hvl1()`` method and see what happens inside to compute the half value layer.
This method is found in the [SpekPy module](https://bitbucket.org/spekpy/spekpy_release/src/master/spekpy/SpekPy.py):

```python
def get_hvl1(self, matl='Al', **kwargs):
    """
    Method to get the first half value layer for a desired material for the
    parameters in the current spekpy state

    :param str matl: The desired material name
    :param kwargs: Keyword arguments to change parameters that are used for
        the calculation
    :return float first_half_value_layer: The calculated first half value
        layer for the desired material [mm]
    """
    calc_params = self.parameters_for_calculation(**kwargs)
    first_half_value_layer = calculate_first_half_value_layer_from_spectrum(self, calc_params, matl)
    return first_half_value_layer
```

It basically calls the method ``calculate_first_half_value_layer_from_spectrum()``, which can be found in the [SpekTools module](https://bitbucket.org/spekpy/spekpy_release/src/master/spekpy/SpekTools.py):

```python
def calculate_first_half_value_layer_from_spectrum(spekpy_obj, calc_params, filter_material):
    """
    A function to calculate the first half value layer of a spectrum for a
    desired material

    :param Spek spekpy_obj: An instance of spekpy object (Spek class)
    :param dict calc_parameters: Ordered dictionary of spectrum parameters
    :param str filter_material: The name of the desired filter material
    :return float first_half_value_layer: The calculated first half value
        layer [mm]
    """
    first_half_value_layer = minimize_for_fraction(spekpy_obj, calc_params,  filter_material, 0.5)
    return first_half_value_layer
```

It basically calls the method ``minimize_for_fraction()``, which can be found in the [SpekTools module](https://bitbucket.org/spekpy/spekpy_release/src/master/spekpy/SpekTools.py):

```python
def minimize_for_fraction(spekpy_obj, calc_params, filter_material,
                          fractional_value):
    """
    A function that is used to calculate the required thickness of a material
    to reach a specified fractional air Kerma value

    :param Spek spekpy_obj: An instance of spekpy object (Spek class)
    :param dict calc_parameters: Ordered dictionary of spectrum parameters
    :param str filter_material: The material of a specified filtration
    :param float fractional_value: The target fractional value for air kerma
    :return float required_filter_thickness: The required thickness of filter
        for the target drop in kerma
    """
    cost_function = make_cost_function_fraction(spekpy_obj, calc_params,
                                            filter_material, fractional_value)
    t = optimize.minimize_scalar(cost_function, method='brent')
    required_filter_thickness = t.x
    return required_filter_thickness
```

It basically calls the method ``make_cost_function_fraction()``, which can be found in the [SpekTools module](https://bitbucket.org/spekpy/spekpy_release/src/master/spekpy/SpekTools.py):

```python
def make_cost_function_fraction(spekpy_obj, calc_params, filter_material,
                                fractional_value):
    """
    A function to create a cost function that can be used to find the filter
    thickness of a specific material to reach a
    specified fraction of air kerma

    :param Spek spekpy_obj: An instance of spekpy object (Spek class)
    :param dict calc_parameters: Ordered dictionary of spectrum parameters
    :param str filter_material: A specified filter material
    :param float fractional_value: A fraction of air Kerma that is desired
    :return cost_function_fraction: The cost function that is used to find the
        required thickness of a specified material needed to reach a specified
        fraction of air kerma
    """
    # free_parameter represents a thickness of filtration
    def cost_function_fraction(free_parameter):
        warnings.filterwarnings("ignore")
        # Store the initial filtration
        state_filtration_original = deepcopy(spekpy_obj.state.filtration)
        d0 = calculate_air_kerma_from_spectrum(spekpy_obj, calc_params,
                                               mas_normalized_air_kerma=False)
        # Filter spectrum with a thickness of free_parameter
        change_filtration(spekpy_obj, filter_material, free_parameter)
        d = calculate_air_kerma_from_spectrum(spekpy_obj, calc_params,
                                              mas_normalized_air_kerma=False)
        # Remove the filtration of thickness free_parameter
        spekpy_obj.state.filtration = state_filtration_original
        if np.isinf(d) or np.isinf(d0):
            val=np.inf
        else:
            val = (fractional_value - d / d0) ** 2
        return val

    return cost_function_fraction
```

What wee see is that, in the end, SpekPy is using the Optimize Module of SciPy, ``scipy.optimize``.
This module is used when you need to optimize the input parameters for a function.
It contains a number of useful methods for optimizing different kinds of functions.
The one SpekPy uses is the ``minimize_scalar()`` function, which is used to minimize a function of one variable.
The SciPy library has three built-in methods for scalar minimization: ``brent``, ``golden`` and ``bounded``.
The one SpekPy is using is the ``brent`` method.
Here's reference material to read:
- [SciPy optimization tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html#univariate-function-minimizers-minimize-scalar)
- [RealPython tutorial on using SciPy for optimization](https://realpython.com/python-scipy-cluster-optimize/#minimizing-a-function-with-one-variable)