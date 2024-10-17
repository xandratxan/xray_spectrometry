###########################################################
# Script to calculate HVL from experimental spectra
###########################################################

import pandas as pd
import math
from scipy.interpolate import Akima1DInterpolator

# 1. We first read the 2 tables: mutr/rho vs E and mu/rho vs E
# Table mutr/rho
logEmutr = []
logmutr = []
archivo_mutr = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\mutr.txt"
with open(archivo_mutr, 'r') as f:
    for linea in f:
        col1 = linea.strip().replace('\t', ' ').split()[0]
        col2 = linea.strip().replace('\t', ' ').split()[1]
        try:
            numeroE = float(col1)
            lnEmutr = math.log(numeroE)
            logEmutr.append(lnEmutr)
            numeromutr = float(col2)
            lnmutr = math.log(numeromutr)
            logmutr.append(lnmutr)
        except ValueError as e:
            print(f'Error: No se puede convertir este valor a float1: {linea}')
            continue

# Table mu/rho
logEmu = []
logmu = []
densityAl = 2.699
archivo_muAl = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_coefficients\muAl.txt"
with open(archivo_muAl, 'r') as f:
    for linea in f:
        col1 = linea.strip().replace('\t', ' ').split()[0]
        col2 = linea.strip().replace('\t', ' ').split()[1]
        try:
            numeroEmu = float(col1)
            lnEmu = math.log(numeroEmu)
            logEmu.append(lnEmu)
            numeromu = float(col2)
            numeromu = numeromu * densityAl
            lnmu = math.log(numeromu)
            logmu.append(lnmu)
        except ValueError as e:
            print(f'Error: No se puede convertir este valor a float2: {linea}')
            continue

# 2. We read the tables of interest: fluence vs E

E = []
logE = []
fluence = []
archivo_fluence = r"C:\Users\u5085\OneDrive\Documents\PAL_2021\CIEMAT\ESTUDIANTES\Estudiante_2023_2\HVL\input_qualities_IR14D_2022\spec30.txt"

with open(archivo_fluence, 'r') as f:
    for linea in f:
        col1 = linea.strip().replace('\t', ' ').split()[0]
        col2 = linea.strip().replace('\t', ' ').split()[1]
        # read the tables of interest: fluence vs E
        numeroE = float(col1)
        E_ln = math.log(numeroE)
        E.append(numeroE)
        logE.append(E_ln)
        numeroflu = float(col2)
        fluence.append(numeroflu)

    # Interpolation Akima mutr/rho and mu
interpolacion_Lnmu = Akima1DInterpolator(logEmu, logmu, axis=0)
interpolacion_Lnmutr = Akima1DInterpolator(logEmutr, logmutr, axis=0)
mu = []
mutr = []
for i in logE:
    try:
        interp_Lnmu = interpolacion_Lnmu(i)
        interp_Lnmutr = interpolacion_Lnmutr(i)
        mu_int = math.exp(interp_Lnmu)
        mutr_int = math.exp(interp_Lnmutr)
        mu.append(mu_int)
        mutr.append(mutr_int)
    except ValueError:
        mu_int.append(float('nan'))

testq = 20.0
delta = testq
ratio = 0.5
while delta > 0.000001:
    delta = delta * 0.5
    # sum over the ratio of the numerator (kerma attenuated) and denominator (kerma no attenuation) = Kratio
    suma_Katt = 0
    suma_K0 = 0
    for i in range(len(E)):
        attenuation = math.exp(-mu[i] * testq)
        Katt = E[i] * fluence[i] * mutr[i] * attenuation
        suma_Katt = suma_Katt + Katt
        K0 = E[i] * fluence[i] * mutr[i]
        suma_K0 = suma_K0 + K0

    trans = suma_Katt / suma_K0

    if abs(trans - ratio) < 0.000005:
        HVL = testq
        break
    if trans > ratio:
        testq = testq + delta
    else:
        testq = testq - delta

print(f'HVL is equal to:  {HVL}')
