###########################################################
# Script to calculate hK from experimental spectra
###########################################################

# IMPORTAR LAS LIBRERIAS NECESARIAS
import math
import os
import random
import statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from scipy import interpolate
from plotnine import *
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from time import time
 
 
 
pantalla = Tk()
pantalla.title("PROGRAMA TOTAL")
 
titulo        = Label(pantalla, text="Programa total", font="Helvetica 20 bold").grid(row=0, columnspan=2, padx=5, pady=5)
 
var_mono      = tk.StringVar()
ruta_mono     = Entry(pantalla, textvariable=var_mono).grid(row=1, column=1, padx=5, pady=5)
boton_mono    = Button(pantalla, text="Seleccionar monos", font="Avantgarde 10 bold", command=lambda: seleccionar_mono()).grid(row=1, column=0, padx=5, pady=5)
 
var_espectros = tk.StringVar()
ruta_espect   = Entry(pantalla, textvariable=var_espectros).grid(row=2, column=1, padx=5, pady=5)
boton_espect  = Button(pantalla, text="Seleccionar espectros", font="Avantgarde 10 bold", command=lambda: seleccionar_espectros()).grid(row=2, column=0, padx=5, pady=5)
 
var_mutrrho   = tk.StringVar()
ruta_mutrrho  = Entry(pantalla, textvariable=var_mutrrho).grid(row=3, column=1, padx=5, pady=5)
boton_mutrrho = Button(pantalla, text="Seleccionar mutr_rho", font="Avantgarde 10 bold", command=lambda: seleccionar_mutrrho()).grid(row=3, column=0, padx=5, pady=5)
 
var_carpeta   = tk.StringVar()
carpeta       = Entry(pantalla, textvariable=var_carpeta).grid(row=4, column=1, padx=5, pady=5)
boton_carpeta = Button(pantalla, text="Seleccionar carpeta para guardar los txt", font="Avantgarde 10 bold", command=lambda: seleccionar_carpeta()).grid(row=4, column=0, padx=5, pady=5)
 
boton_princip = Button(pantalla, text="EJECUTAR", font="Avantgarde 20 bold", background="lightblue", command=lambda: programa_principal()).grid(row=5, columnspan=2, padx=5, pady=5)
 
 
 
lista_mono      = []
lista_espectros = []
directorio      = tk.StringVar()
directorio2     = tk.StringVar()
 
 
 
#PAL:dialog box para entrada de los coef monoenergéticos para diferentes ángulos
def seleccionar_mono():
    ruta_mono = filedialog.askopenfilenames()
    var_mono.set(ruta_mono)
    
    for x in ruta_mono:
        lista_mono.append(os.path.basename(x))
        directorio.set(os.path.dirname(x))
        #print("Directorio actual:", directorio.get())
 
 
#PAL:dialog box para entrada de los espectros medidos
def seleccionar_espectros():
    ruta_espect = filedialog.askopenfilenames()
    var_espectros.set(ruta_espect)
    
    for x in ruta_espect:
        lista_espectros.append(os.path.basename(x))
        directorio2.set(os.path.dirname(x))
        #print("Directorio actual:", directorio2.get())
 
 
#PAL:entrada del fichero de mass energy transfer coefficient
def seleccionar_mutrrho():
    ruta_mutrrho = filedialog.askopenfilename()
    var_mutrrho.set(ruta_mutrrho)
 
 
#PAL: dialog box para selección de la carpeta del output    
def seleccionar_carpeta():
    ruta_carpeta = filedialog.askdirectory()
    var_carpeta.set(ruta_carpeta)
 
 
 
# FUNCIÓN PARA BUSCAR UN ARCHIVO Y ELIMINARLO SI YA EXISTE
def buscar_eliminar(ruta):
    if os.path.exists(ruta):
        #print("funcion buscar eliminar ruta", ruta)
        os.remove(ruta)
    else:
        print("")
 
 
 
# FUNCIÓN PARA TRANSFORMAR UN DATAFRAME A TXT Y GUARDARLO
# PAL: media: valor medio de la energía en el espectro; desviacion: desviación típica; v_hpk: coeficiente de variación de la energía
def guardar_txt(ruta, nombre, media, angulo, desviacion, v_hpk):
    x = pd.DataFrame({"_Nombre":[nombre], "_Media_Espectro_"+angulo:[media], "______Desviación______":[desviacion], "_______V_HPK_______":[v_hpk]})
    x.to_csv(ruta, header=not (os.path.isfile(ruta) and os.stat(ruta).st_size != 0), index=False, mode="a", sep=",")
 
 
 
 
def programa_principal():
 
# PAL: me gustaría que estas var fuesen un input
    # DECLARAR VARIABLES
    n      = 1*10**2                 #Pablo n      = 1*10**6
    umutrr = 0.017
    uEr    = 0.01
    uflur  = 0.01
    uhk = 0.01 # PAL: me gustaría asociar una incertidumbre al coef monoenergético    
# PAL: me gustaría eliminar la variable kerma...
    ukerma = 0.01
 
 
 
 
    # CREAR DIRECTORIO PARA GUARDAR LOS FICHEROS DE SALIDA
    ruta = var_carpeta.get()
    Path(ruta).mkdir(parents=True, exist_ok=True)
    #print("ruta directorio guardar ficheros", ruta)
 
 
    # ARRAY CON LOS NOMBRES DE LOS FICHEROS DE ESPECTRO Y MONOENERGÉTICOS
    #ficheros_espectros       = ["N60.csv", "N20.csv"]
    #ficheros_espectros       = ["N15.csv", "N20.csv"]
    #ficheros_monoenergeticos = ["h_amb_10.csv", "hp_10_slab.csv", "hp_3_cyl.csv", "h_prime_3.csv"]
    #ficheros_monoenergeticos = ["hp_0.07_slab.csv", "h_prime_0.07.csv", "h_prime_3.csv", "hp_3_cyl.csv", "hp_10_slab.csv"]
    #ficheros_monoenergeticos = ["h_prime_3.csv", "h_prime_0.07.csv"]
    #ficheros_monoenergeticos = ["hp_10_slab.csv"]
    #ficheros_monoenergeticos = ["hp_3_cyl.csv"]
    
    ficheros_espectros       = lista_espectros # PAL: lista de los espectros (pueden llegar a ser 52)
    ficheros_monoenergeticos = lista_mono # PAL: lista de los coef monoenergéticos (8 diferentes según ángulos)
 
 
    #print("Directorio actual:", directorio.get())
    # LEER EL FICHERO MONOENERGÉTICO
    for f_m in ficheros_monoenergeticos:
        hk_table = pd.read_csv(directorio.get()+"/"+f_m, sep=";", encoding = 'ISO-8859-1')
        #print("Directorio actual hktable:", directorio.get())
        #print("ruta para eliminar archivos", ruta)
        buscar_eliminar(ruta+"/"+f_m.upper()+".txt")
        #print("Buscar_eliminar _0txt", ruta+"/"+f_m.upper()+"_0.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_0.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_15.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_30.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_45.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_60.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_75.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_90.txt")
        buscar_eliminar(ruta+"/"+f_m.upper()+"_180.txt")
 
###############################################################################################################
# FIRST LOOP IN monoenergetic tables for the ISO conversion coefficients at incident angle = 0
# ("h_amb_10.csv","hp_0.07_pill.csv", "hp_0.07_rod.csv")
###############################################################################################################
        # COMPROBAR QUE EL FICHERO TENGA MENOS DE 2 COLUMNAS
        if len(hk_table.columns) <= 2:
            tiempo_inicial_columns_2 = time()
            #print("contenido de hk_table:", hk_table)
 
 
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MONOENERGÉTICOS
            Ehk = hk_table.iloc[:, 0].values
            hk  = hk_table.iloc[:, 1].values
            #print("Contenido de Ehk", Ehk)
            #print("Contenido de hk", hk)
            # REALIZAR LOS LOGARITMOS
            LEhk = []
            Lhk  = []
 
            for x in Ehk:
                LEhk.append(math.log(x))
 
            for x in hk:
                Lhk.append(math.log(x))
 
            #print("Contenido de LEhk", LEhk)
            #print("Contenido de Lhk", Lhk)
            # LEER EL FICHERO MUTR_RHO  
            mutr_rho = pd.read_csv(var_mutrrho.get(), sep="\t", header=None, encoding='ISO-8859-1')
            #print("Contenido de mutr_rho", mutr_rho)
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MUTR_RHO
            E_mut_aux = mutr_rho.iloc[:, 0].values
            mtr_aux = mutr_rho.iloc[:, 1].values
            #print("Contenido de E_mut_aux", E_mut_aux)
            #print("Contenido de mtr_aux", mtr_aux)
            E_mut = []
            mtr = []
 
            # REEMPLAZAR LOS PUNTOS POR COMAS
            for x in E_mut_aux:
                E_mut.append(float(x))
 
            for x in mtr_aux:
                mtr.append(float(x))
            #print("contenido de E_mut:", E_mut)
            #print("contenido de mtr:", mtr)
            # REALIZAR LOS LOGARITMOS
            LE_mut = [math.log(x) for x in E_mut]
            Lmtr = [math.log(x) for x in mtr]
            #print("Contenido de LE_mut:", LE_mut)
            #print("Contenido de Lmtr:", Lmtr)
 
 
            # LEER EL FICHERO ESPECTRO
            for f_e in ficheros_espectros:
                espectro = pd.read_csv(directorio2.get()+"/"+f_e, sep=",")
                #print("Directorio actual:", directorio2.get())
 
 
                # GUARDAR EN VARIABLES LOS VALORES DEL CSV ESPECTROS
                E        = espectro.iloc[:, 0].values
                fluencia = espectro.iloc[:, 1].values
                kerma    = espectro.iloc[:, 2].values #PAL: quiero eliminar esta variable
                nfilas   = len(fluencia)
                #print("Contenido de E", E)
                #print("Contenido de fluencia", fluencia)
                #print("Contenido de kerma", kerma)
                #nfilas   = len(fluencia) #entrada del número de fila para crear la distribución pseudoaleatoria
 
                # Realizar EL LOGARITMO
                LE = []
                for x in E:
                    LE.append(math.log(x))
 
                
                # RELIZAR INTERPOLACIÓN CON MUTR_RHO
                if len(LE_mut) < 2:
                    print("Error: LE_mut debe contener al menos 2 elementos para la interpolación.")
                else:
                    interpolacion_uno_mut = interpolate.Akima1DInterpolator(LE_mut, Lmtr, axis=0)
                ln_p_int = []
 
                for i in LE:
                    interpolacion_final_mut = math.exp(interpolacion_uno_mut(i))
                    ln_p_int.append(interpolacion_final_mut)
 
                p_int = ln_p_int
 
                #print("contenido p_int", p_int)
                # REALIZAR INTERPOLACIÓN CON HK
                interpolacion_uno_hk = interpolate.Akima1DInterpolator(LEhk, Lhk, axis=0)
                ln_hk_int = []
 
                for i in LE:
                    interpolacion_final_hk = math.exp(interpolacion_uno_hk(i))
                    ln_hk_int.append(interpolacion_final_hk)
 
                hk_int = ln_hk_int
                #print("contenido hk_int", hk_int)
# CÁLCULO DE INCERTIDUMBRES:
                # DECLARAR MATRICES Y VECTORES
                Emat     = np.zeros((nfilas, n))
                flumat   = np.zeros((nfilas, n))
                mutrmat  = np.zeros((nfilas, n))
# PAL           hkmat    = np.zeros((nfilas, n)) 
                #print("contenido Emat", Emat)
                nhpk = np.zeros(shape=n)
                dhpk = np.zeros(shape=n)
                hpk  = np.zeros(shape=n)
 
 
                for j in range(n):
                    nhpk[j] = 0.0
                    dhpk[j] = 0.0
 
                    for i in range(nfilas):
                        Emat[i,j]    = np.random.normal(E[i], uEr*E[i], 1)
                        flumat[i,j]  = np.random.normal(fluencia[i], uflur*fluencia[i], 1)
                        mutrmat[i,j] = np.random.normal(p_int[i], umutrr*p_int[i], 1)
# PAL                   hkmat[i,j]   = np.random.normal(hk_int[i], uhk*hk_int[i], 1)
 
                        nhpk[j] = nhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int[i])
# PAL                   nhpk[j] = nhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hkmat[i])
                        dhpk[j] = dhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j])
                        hpk[j]  = nhpk[j]/dhpk[j]
 
 
                np.set_printoptions(linewidth=np.inf)
                print("")
                print("---------- ESPECTROS SIN ÁNGULOS ----------")     
 
 
                # MEDIA DEL ESPECTRO
                media_espectro = statistics.mean(hpk)
                sd_hpk         = statistics.pstdev(hpk)
                v_hpk          = sd_hpk*100/media_espectro
                
#                plt.hist(hpk, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK.pdf')
 
                print("|Fichero monoenergético:",f_m)
                print("|Fichero espectro:",f_e) 
                print("|Valor medio del espectro leído:",media_espectro)
                print("|Desviación del espectro:",sd_hpk)
                print("|V_HPK:",v_hpk)
 
                ruta_final = ruta+"/"+f_m.upper()+".txt"
 
                x = pd.DataFrame({"_Nombre":[f_e],"__Media_Espectro__":[media_espectro], "______Desviación______":[sd_hpk], "_______V_HPK_______":[v_hpk]})
                x.to_csv(ruta_final, header=not (os.path.isfile(ruta_final) and os.stat(ruta_final).st_size != 0), index=False, mode="a", sep=",")
 
                tiempo_final_columns_2 = time() 
 
                tiempo_ejecucion_columns_2 = tiempo_final_columns_2 - tiempo_inicial_columns_2
 
                print ('El tiempo de ejecucion para hktable columns 2 fue:',tiempo_ejecucion_columns_2)
###############################################################################################################
# SECOND LOOP IN the monoenergetic tables for the ISO conversion coefficients at 6 incident angles: 0 -750
#("hp_10_slab.csv","hp_0.07_slab.csv")
###############################################################################################################
        elif len(hk_table.columns) == 7:
            tiempo_inicial_columns_7 = time()
 
            # GUARDAR EN VARIABLES LOS VALORES DEL FICHERO MONOENERGÉTICO
            Ehk   = hk_table.iloc[:, 0].values
            hk_0  = hk_table.iloc[:, 1].values
            hk_15 = hk_table.iloc[:, 2].values
            hk_30 = hk_table.iloc[:, 3].values
            hk_45 = hk_table.iloc[:, 4].values
            hk_60 = hk_table.iloc[:, 5].values
            hk_75 = hk_table.iloc[:, 6].values
 
 
            # REALIZAR LOGARITMOS
            LEhk    = []
            Lhk_0   = []
            Lhk_15  = []
            Lhk_30  = []
            Lhk_45  = []
            Lhk_60  = []
            Lhk_75  = []
 
            for x in Ehk:
                LEhk.append(math.log(x))
 
            for x in hk_0:
                if x !=0:
                    Lhk_0.append(math.log(x))
                else:
                    Lhk_0.append(x)
 
            for x in hk_15:
                if x !=0:
                    Lhk_15.append(math.log(x))
                else:
                    Lhk_15.append(x)
 
            for x in hk_30:
                if x !=0:
                    Lhk_30.append(math.log(x))
                else:
                    Lhk_30.append(x)
 
            for x in hk_45:
                if x !=0:
                    Lhk_45.append(math.log(x))
                else:
                    Lhk_45.append(x)
 
            for x in hk_60:
                if x !=0:
                    Lhk_60.append(math.log(x))
                else:
                    Lhk_60.append(x)
 
            for x in hk_75:
                if x !=0:
                    Lhk_75.append(math.log(x))
                else:
                    Lhk_75.append(x)
 
 
 
            # LEER EL FICHERO MUTR_RHO  
            mutr_rho = pd.read_csv(var_mutrrho.get(), sep="\t", header=None, encoding='ISO-8859-1')
 
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MUTR_RHO
            E_mut_aux = mutr_rho.iloc[:, 0].values
            mtr_aux = mutr_rho.iloc[:, 1].values
 
            E_mut = []
            mtr = []
 
            # REEMPLAZAR LOS PUNTOS POR COMAS
            for x in E_mut_aux:
                    E_mut.append(float(x))
 
            for x in mtr_aux:
                    mtr.append(float(x))
 
            # REALIZAR LOS LOGARITMOS
            LE_mut = [math.log(x) for x in E_mut]
            Lmtr = [math.log(x) for x in mtr]
 
 
            # LEER EL FICHERO ESPECTROS
            for f_e in ficheros_espectros:
                espectro = pd.read_csv(directorio2.get()+"/"+f_e, sep=",")
                #print("mi direcorio actual de espectro es:", directorio2.get())
 
                # GUARDAR EN VARIABLES LOS VALORES DEL CSV ESPECTROS
                E        = espectro.iloc[:, 0].values
                fluencia = espectro.iloc[:, 1].values
                kerma    = espectro.iloc[:, 2].values #PAL: quiero eliminar esta variable
                nfilas   = len(fluencia)
                #print("Contenido de E-2", E)
                #print("Contenido de fluencia-2", fluencia)
                #print("Contenido de kerma-2", kerma)
 
 
                # REALIZAR INTERPOLACIÓN
                LE = []
                for x in E:
                    LE.append(math.log(x))
 
                #print("Contenido LE_mut angulos 75", LE_mut)
                #print("Contenido Lmtr angulos 75", Lmtr)
                # REALIZAR INTERPOLACIÓN CON MUTR_RHO
                if len(LE_mut) < 2:
                    print("Error: LE_mut debe contener al menos 2 elementos para la interpolación.")
                else:
                    interpolacion_uno_mut = interpolate.Akima1DInterpolator(LE_mut, Lmtr, axis=0)
                ln_p_int = []
 
                for i in LE:
                    interpolacion_final_mut = math.exp(interpolacion_uno_mut(i))
                    ln_p_int.append(interpolacion_final_mut)
 
                p_int = ln_p_int
 
 
                # REALIZAR INTERPOLACIÓN CON HK
                interpolacion_uno_0  = interpolate.Akima1DInterpolator(LEhk, Lhk_0, axis=0)
                interpolacion_uno_15 = interpolate.Akima1DInterpolator(LEhk, Lhk_15, axis=0)
                interpolacion_uno_30 = interpolate.Akima1DInterpolator(LEhk, Lhk_30, axis=0)
                interpolacion_uno_45 = interpolate.Akima1DInterpolator(LEhk, Lhk_45, axis=0)
                interpolacion_uno_60 = interpolate.Akima1DInterpolator(LEhk, Lhk_60, axis=0)
                interpolacion_uno_75 = interpolate.Akima1DInterpolator(LEhk, Lhk_75, axis=0)
 
                hk_int_0   = []
                hk_int_15  = []
                hk_int_30  = []
                hk_int_45  = []
                hk_int_60  = []
                hk_int_75  = []
 
                for i in LE:
                    interpolacion_final_0  = math.exp(interpolacion_uno_0(i))
                    hk_int_0.append(interpolacion_final_0)
 
                    interpolacion_final_15 = math.exp(interpolacion_uno_15(i))
                    hk_int_15.append(interpolacion_final_15)
 
                    interpolacion_final_30 = math.exp(interpolacion_uno_30(i))
                    hk_int_30.append(interpolacion_final_30)
 
                    interpolacion_final_45 = math.exp(interpolacion_uno_45(i))
                    hk_int_45.append(interpolacion_final_45)
 
                    interpolacion_final_60 = math.exp(interpolacion_uno_60(i))
                    hk_int_60.append(interpolacion_final_60)
 
                    interpolacion_final_75 = math.exp(interpolacion_uno_75(i))
                    hk_int_75.append(interpolacion_final_75)
 
 
 
                # DECLARAR MATRICES Y VECTORES
                Emat    = np.zeros((nfilas, n))
                flumat  = np.zeros((nfilas, n))
                mutrmat = np.zeros((nfilas, n))
 
                dhpk     = np.zeros(shape=n)
                nhpk_0   = np.zeros(shape=n)
                nhpk_15  = np.zeros(shape=n)
                nhpk_30  = np.zeros(shape=n)
                nhpk_45  = np.zeros(shape=n)
                nhpk_60  = np.zeros(shape=n)
                nhpk_75  = np.zeros(shape=n)
                hpk_0    = np.zeros(shape=n)
                hpk_15   = np.zeros(shape=n)
                hpk_30   = np.zeros(shape=n)
                hpk_45   = np.zeros(shape=n)
                hpk_60   = np.zeros(shape=n)
                hpk_75   = np.zeros(shape=n)
 
                for j in range(n):
                    nhpk_0[j]  = 0.0
                    nhpk_15[j] = 0.0
                    nhpk_30[j] = 0.0
                    nhpk_45[j] = 0.0
                    nhpk_60[j] = 0.0
                    nhpk_75[j] = 0.0
                    dhpk[j]    = 0.0
 
                    for i in range(nfilas):
                        Emat[i,j]    = np.random.normal(E[i], uEr*E[i], 1)
                        flumat[i,j]  = np.random.normal(fluencia[i], uflur*fluencia[i], 1)
                        mutrmat[i,j] = np.random.normal(p_int[i], umutrr*p_int[i], 1)
 
                        nhpk_0[j]  = nhpk_0[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_0[i])
                        nhpk_15[j] = nhpk_15[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_15[i])
                        nhpk_30[j] = nhpk_30[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_30[i])
                        nhpk_45[j] = nhpk_45[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_45[i])
                        nhpk_60[j] = nhpk_60[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_60[i])
                        nhpk_75[j] = nhpk_75[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_75[i])
 
                        dhpk[j]    = dhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j])
 
                        hpk_0[j]  = nhpk_0[j]/dhpk[j]
                        hpk_15[j] = nhpk_15[j]/dhpk[j]
                        hpk_30[j] = nhpk_30[j]/dhpk[j]
                        hpk_45[j] = nhpk_45[j]/dhpk[j]
                        hpk_60[j] = nhpk_60[j]/dhpk[j]
                        hpk_75[j] = nhpk_75[j]/dhpk[j]
 
                np.set_printoptions(linewidth=np.inf)
                print("")
                print("---------- ESPECTROS ANGULOS 75º ----------")     
 
                # MEDIA DEL ESPECTRO
                media_espectro_0 = statistics.mean(hpk_0)
                media_espectro_15 = statistics.mean(hpk_15)
                media_espectro_30 = statistics.mean(hpk_30)
                media_espectro_45 = statistics.mean(hpk_45)
                media_espectro_60 = statistics.mean(hpk_60)
                media_espectro_75 = statistics.mean(hpk_75)
                
                sd_hpk_0          = statistics.pstdev(hpk_0)
                sd_hpk_15         = statistics.pstdev(hpk_15)
                sd_hpk_30         = statistics.pstdev(hpk_30)
                sd_hpk_45         = statistics.pstdev(hpk_45)
                sd_hpk_60         = statistics.pstdev(hpk_60)
                sd_hpk_75         = statistics.pstdev(hpk_75)
                
                v_hpk_0           = sd_hpk_0*100/media_espectro_0
                v_hpk_15          = sd_hpk_15*100/media_espectro_15
                v_hpk_30          = sd_hpk_30*100/media_espectro_30
                v_hpk_45          = sd_hpk_45*100/media_espectro_45
                v_hpk_60          = sd_hpk_60*100/media_espectro_60
                v_hpk_75          = sd_hpk_75*100/media_espectro_75
                
                # sns.histplot(hpk_0, color="red", kde=True, linewidth=1)
                # plt.show()
                # sns.histplot(hpk_15, color="red", kde=True, linewidth=1)
                # plt.show()
                # sns.histplot(hpk_30, color="red", kde=True, linewidth=1)
                # plt.show()
                # sns.histplot(hpk_45, color="red", kde=True, linewidth=1)
                # plt.show()
                # sns.histplot(hpk_60, color="red", kde=True, linewidth=1)
                # plt.show()
                # sns.histplot(hpk_75, color="red", kde=True, linewidth=1)
                # plt.show()
                
#                plt.hist(hpk_0, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK_0.pdf')

#                plt.hist(hpk_15, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#               plt.savefig('HPK_15.pdf')

#                plt.hist(hpk_30, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK_30.pdf')
                
#                plt.hist(hpk_45, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK_45.pdf')
                
#                plt.hist(hpk_60, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK_60.pdf')
                
#                plt.hist(hpk_75, 400, edgecolor="black", linewidth=1.2)
#                plt.show()
#                plt.savefig('HPK_75.pdf')
                
                print("|Fichero monoenergético:",f_m)
                print("|Fichero espectro:",f_e)  
                
                print("|Valor medio del espectro leído 0º:",media_espectro_0)
                print("|Valor medio del espectro leído 15º:",media_espectro_15)
                print("|Valor medio del espectro leído 30º:",media_espectro_30)
                print("|Valor medio del espectro leído 45º:",media_espectro_45)
                print("|Valor medio del espectro leído 60º:",media_espectro_60)
                print("|Valor medio del espectro leído 75º:",media_espectro_75)
                
                print("|Desviación del espectro 0º:",sd_hpk_0)
                print("|Desviación del espectro 15º:",sd_hpk_15)
                print("|Desviación del espectro 30º:",sd_hpk_30)
                print("|Desviación del espectro 45º:",sd_hpk_45)
                print("|Desviación del espectro 60º:",sd_hpk_60)
                print("|Desviación del espectro 75º:",sd_hpk_75)
                
                print("|V_HPK 0º:",v_hpk_0)
                print("|V_HPK 15º:",v_hpk_15)
                print("|V_HPK 30º:",v_hpk_30)
                print("|V_HPK 45º:",v_hpk_45)
                print("|V_HPK 60º:",v_hpk_60)
                print("|V_HPK 75º:",v_hpk_75)
 
                guardar_txt(ruta+"/"+f_m.upper()+"_0.txt", f_e, media_espectro_0, "0", sd_hpk_0, v_hpk_0)
                guardar_txt(ruta+"/"+f_m.upper()+"_15.txt", f_e, media_espectro_15, "15", sd_hpk_15, v_hpk_15)
                guardar_txt(ruta+"/"+f_m.upper()+"_30.txt", f_e, media_espectro_30, "30", sd_hpk_30, v_hpk_30)
                guardar_txt(ruta+"/"+f_m.upper()+"_45.txt", f_e, media_espectro_45, "45", sd_hpk_45, v_hpk_45)
                guardar_txt(ruta+"/"+f_m.upper()+"_60.txt", f_e, media_espectro_60, "60", sd_hpk_60, v_hpk_60)
                guardar_txt(ruta+"/"+f_m.upper()+"_75.txt", f_e, media_espectro_75, "75", sd_hpk_75, v_hpk_75)
                
                tiempo_final_columns_7 = time() 
 
                tiempo_ejecucion_columns_7 = tiempo_final_columns_7 - tiempo_inicial_columns_7
 
                print ('El tiempo de ejecucion para hktable columns 7 fue:',tiempo_ejecucion_columns_7)
 
###############################################################################################################
# THRID LOOP IN the monoenergetic tables for the ISO conversion coefficient at 7 incident angles: 0 -900
# ("hp_3_cyl.csv")
###############################################################################################################
        elif len(hk_table.columns) == 8:
            tiempo_inicial_columns_8 = time()
 
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MONOENERGÉTICO
 
            Ehk   = hk_table.iloc[:, 0].values
            hk_0  = hk_table.iloc[:, 1].values
            hk_15 = hk_table.iloc[:, 2].fillna(value=0).values
            hk_30 = hk_table.iloc[:, 3].fillna(value=0).values
            hk_45 = hk_table.iloc[:, 4].fillna(value=0).values
            hk_60 = hk_table.iloc[:, 5].fillna(value=0).values
            hk_75 = hk_table.iloc[:, 6].fillna(value=0).values
            hk_90 = hk_table.iloc[:, 7].fillna(value=0).values
 
 
            # REALIZAR LOGARITMOS
            LEhk    = []
            Lhk_0   = []
            Lhk_15  = []
            Lhk_30  = []
            Lhk_45  = []
            Lhk_60  = []
            Lhk_75  = []
            Lhk_90  = []
 
            for x in Ehk:
                LEhk.append(math.log(x))
 
            for x in hk_0:
                if x !=0:
                    Lhk_0.append(math.log(x))
                else:
                    Lhk_0.append(x)
 
            for x in hk_15:
                if x !=0:
                    Lhk_15.append(math.log(x))
                else:
                    Lhk_15.append(x)
 
            for x in hk_30:
                if x !=0:
                    Lhk_30.append(math.log(x))
                else:
                    Lhk_30.append(x)
 
            for x in hk_45:
                if x !=0:
                    Lhk_45.append(math.log(x))
                else:
                    Lhk_45.append(x)
 
            for x in hk_60:
                if x !=0:
                    Lhk_60.append(math.log(x))
                else:
                    Lhk_60.append(x)
 
            for x in hk_75:
                if x !=0:
                    Lhk_75.append(math.log(x))
                else:
                    Lhk_75.append(x)
 
            for x in hk_90:
                if x !=0:
                    Lhk_90.append(math.log(x))
                else:
                    Lhk_90.append(x)
 
 
 
 
            # LEER EL FICHERO MUTR_RHO  
            mutr_rho = pd.read_csv(var_mutrrho.get(), sep="\t", header=None, encoding='ISO-8859-1')
 
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MUTR_RHO
            E_mut_aux = mutr_rho.iloc[:, 0].values
            mtr_aux = mutr_rho.iloc[:, 1].values
 
            E_mut = []
            mtr = []
 
            # REEMPLAZAR LOS PUNTOS POR COMAS
            for x in E_mut_aux:
                    E_mut.append(float(x))
 
            for x in mtr_aux:
                    mtr.append(float(x))
 
            # REALIZAR LOS LOGARITMOS
            LE_mut = [math.log(x) for x in E_mut]
            Lmtr = [math.log(x) for x in mtr]
 
 
 
            # LEER EL FICHERO ESPECTROS
            for f_e in ficheros_espectros:
                espectro = pd.read_csv(directorio2.get()+"/"+f_e, sep=",")
 
 
                # GUARDAR EN VARIABLES LOS VALORES DEL CSV ESPECTROS
                E        = espectro.iloc[:, 0].values
                fluencia = espectro.iloc[:, 1].values
                kerma    = espectro.iloc[:, 2].values
                nfilas   = len(fluencia)
 
                # REALIZAR INTERPOLACIONES
                LE = []
                for x in E:
                    LE.append(math.log(x))
 
                #print("Contenido LE_mut angulos hk= 8 columns", LE_mut)
                #print("Contenido Lmtr angulos hk= 8 columns", Lmtr)
                # REALIZAR INTERPOLACIÓN CON MUTR_RHO
                if len(LE_mut) < 2:
                    print("Error: LE_mut debe contener al menos 2 elementos para la interpolación.")
                else:
                    interpolacion_uno_mut = interpolate.Akima1DInterpolator(LE_mut, Lmtr, axis=0)
                ln_p_int = []
 
                for i in LE:
                    interpolacion_final_mut = math.exp(interpolacion_uno_mut(i))
                    ln_p_int.append(interpolacion_final_mut)
 
                p_int = ln_p_int
 
 
                # REALIZAR INTERPOLACIÓN CON HK          
                interpolacion_uno_hk_0  = interpolate.Akima1DInterpolator(LEhk, Lhk_0, axis=0)
                interpolacion_uno_hk_15 = interpolate.Akima1DInterpolator(LEhk, Lhk_15, axis=0)
                interpolacion_uno_hk_30 = interpolate.Akima1DInterpolator(LEhk, Lhk_30, axis=0)
                interpolacion_uno_hk_45 = interpolate.Akima1DInterpolator(LEhk, Lhk_45, axis=0)
                interpolacion_uno_hk_60 = interpolate.Akima1DInterpolator(LEhk, Lhk_60, axis=0)
                interpolacion_uno_hk_75 = interpolate.Akima1DInterpolator(LEhk, Lhk_75, axis=0)
                interpolacion_uno_hk_90 = interpolate.Akima1DInterpolator(LEhk, Lhk_90, axis=0)
 
                hk_int_0  = []
                hk_int_15 = []
                hk_int_30 = []
                hk_int_45 = []
                hk_int_60 = []
                hk_int_75 = []
                hk_int_90 = []
 
                for i in LE:
                    interpolacion_final_hk_0  = math.exp(interpolacion_uno_hk_0(i))
                    hk_int_0.append(interpolacion_final_hk_0)
 
                    interpolacion_final_hk_15 = math.exp(interpolacion_uno_hk_15(i))
                    hk_int_15.append(interpolacion_final_hk_15)
 
                    interpolacion_final_hk_30 = math.exp(interpolacion_uno_hk_30(i))
                    hk_int_30.append(interpolacion_final_hk_30)
 
                    interpolacion_final_hk_45 = math.exp(interpolacion_uno_hk_45(i))
                    hk_int_45.append(interpolacion_final_hk_45)
 
                    interpolacion_final_hk_60 = math.exp(interpolacion_uno_hk_60(i))
                    hk_int_60.append(interpolacion_final_hk_60)
 
                    interpolacion_final_hk_75 = math.exp(interpolacion_uno_hk_75(i))
                    hk_int_75.append(interpolacion_final_hk_75)
 
                    interpolacion_final_hk_90 = math.exp(interpolacion_uno_hk_90(i))
                    hk_int_90.append(interpolacion_final_hk_90)
 
 
                # DECLARAR MATRICES Y VECTORES
                Emat    = np.zeros((nfilas, n))
                flumat  = np.zeros((nfilas, n))
                mutrmat = np.zeros((nfilas, n))
 
                dhpk     = np.zeros(shape=n)
                nhpk_0   = np.zeros(shape=n)
                nhpk_15  = np.zeros(shape=n)
                nhpk_30  = np.zeros(shape=n)
                nhpk_45  = np.zeros(shape=n)
                nhpk_60  = np.zeros(shape=n)
                nhpk_75  = np.zeros(shape=n)
                nhpk_90  = np.zeros(shape=n)
                hpk_0    = np.zeros(shape=n)
                hpk_15   = np.zeros(shape=n)
                hpk_30   = np.zeros(shape=n)
                hpk_45   = np.zeros(shape=n)
                hpk_60   = np.zeros(shape=n)
                hpk_75   = np.zeros(shape=n)
                hpk_90   = np.zeros(shape=n)
 
                for j in range(n):
                    nhpk_0[j]  = 0.0
                    nhpk_15[j] = 0.0
                    nhpk_30[j] = 0.0
                    nhpk_45[j] = 0.0
                    nhpk_60[j] = 0.0
                    nhpk_75[j] = 0.0
                    nhpk_90[j] = 0.0
                    dhpk[j]    = 0.0
 
                    for i in range(nfilas):
                        Emat[i,j]    = np.random.normal(E[i], uEr*E[i], 1)
                        flumat[i,j]  = np.random.normal(fluencia[i], uflur*fluencia[i], 1)
                        mutrmat[i,j] = np.random.normal(p_int[i], umutrr*p_int[i], 1)
 
                        nhpk_0[j]  = nhpk_0[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_0[i])
                        nhpk_15[j] = nhpk_15[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_15[i])
                        nhpk_30[j] = nhpk_30[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_30[i])
                        nhpk_45[j] = nhpk_45[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_45[i])
                        nhpk_60[j] = nhpk_60[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_60[i])
                        nhpk_75[j] = nhpk_75[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_75[i])
                        nhpk_90[j] = nhpk_90[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_90[i])
 
                        dhpk[j]    = dhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j])
 
                        hpk_0[j]  = nhpk_0[j]/dhpk[j]
                        hpk_15[j] = nhpk_15[j]/dhpk[j]
                        hpk_30[j] = nhpk_30[j]/dhpk[j]
                        hpk_45[j] = nhpk_45[j]/dhpk[j]
                        hpk_60[j] = nhpk_60[j]/dhpk[j]
                        hpk_75[j] = nhpk_75[j]/dhpk[j]
                        hpk_90[j] = nhpk_90[j]/dhpk[j]
 
                np.set_printoptions(linewidth=np.inf)
                print("")
                print("---------- ESPECTROS ANGULOS 90º ----------")     
 
 
                # MEDIA DEL ESPECTRO
                media_espectro_0 = statistics.mean(hpk_0)
                media_espectro_15 = statistics.mean(hpk_15)
                media_espectro_30 = statistics.mean(hpk_30)
                media_espectro_45 = statistics.mean(hpk_45)
                media_espectro_60 = statistics.mean(hpk_60)
                media_espectro_75 = statistics.mean(hpk_75)
                media_espectro_90 = statistics.mean(hpk_90)
                
                sd_hpk_0          = statistics.pstdev(hpk_0)
                sd_hpk_15         = statistics.pstdev(hpk_15)
                sd_hpk_30         = statistics.pstdev(hpk_30)
                sd_hpk_45         = statistics.pstdev(hpk_45)
                sd_hpk_60         = statistics.pstdev(hpk_60)
                sd_hpk_75         = statistics.pstdev(hpk_75)
                sd_hpk_90         = statistics.pstdev(hpk_90)
                
                v_hpk_0           = sd_hpk_0*100/media_espectro_0
                v_hpk_15          = sd_hpk_15*100/media_espectro_15
                v_hpk_30          = sd_hpk_30*100/media_espectro_30
                v_hpk_45          = sd_hpk_45*100/media_espectro_45
                v_hpk_60          = sd_hpk_60*100/media_espectro_60
                v_hpk_75          = sd_hpk_75*100/media_espectro_75
                v_hpk_90          = sd_hpk_90*100/media_espectro_90
                
                # plt.hist(hpk_0, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_0.pdf')
                #
                # plt.hist(hpk_15, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_15.pdf')
                
                # plt.hist(hpk_30, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_30.pdf')
                #
                # plt.hist(hpk_45, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_45.pdf')
                #
                # plt.hist(hpk_60, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_60.pdf')
                #
                # plt.hist(hpk_75, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_75.pdf')
                #
                # plt.hist(hpk_90, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_90.pdf')
                
                print("|Fichero monoenergético:",f_m)
                print("|Fichero espectro:",f_e)
                
                print("|Valor medio del espectro leído 0º:",media_espectro_0)
                print("|Valor medio del espectro leído 15º:",media_espectro_15)
                print("|Valor medio del espectro leído 30º:",media_espectro_30)
                print("|Valor medio del espectro leído 45º:",media_espectro_45)
                print("|Valor medio del espectro leído 60º:",media_espectro_60)
                print("|Valor medio del espectro leído 75º:",media_espectro_75)
                print("|Valor medio del espectro leído 75º:",media_espectro_90)
                
                print("|Desviación del espectro 0º:",sd_hpk_0)
                print("|Desviación del espectro 15º:",sd_hpk_15)
                print("|Desviación del espectro 30º:",sd_hpk_30)
                print("|Desviación del espectro 45º:",sd_hpk_45)
                print("|Desviación del espectro 60º:",sd_hpk_60)
                print("|Desviación del espectro 75º:",sd_hpk_75)
                print("|Desviación del espectro 90º:",sd_hpk_90)
                
                print("|V_HPK 0º:",v_hpk_0)
                print("|V_HPK 15º:",v_hpk_15)
                print("|V_HPK 30º:",v_hpk_30)
                print("|V_HPK 45º:",v_hpk_45)
                print("|V_HPK 60º:",v_hpk_60)
                print("|V_HPK 75º:",v_hpk_75)
                print("|V_HPK 90º:",v_hpk_90)
 
                guardar_txt(ruta+"/"+f_m.upper()+"_0.txt", f_e, media_espectro_0, "0", sd_hpk_0, v_hpk_0)
                guardar_txt(ruta+"/"+f_m.upper()+"_15.txt", f_e, media_espectro_15, "15", sd_hpk_15, v_hpk_15)
                guardar_txt(ruta+"/"+f_m.upper()+"_30.txt", f_e, media_espectro_30, "30", sd_hpk_30, v_hpk_30)
                guardar_txt(ruta+"/"+f_m.upper()+"_45.txt", f_e, media_espectro_45, "45", sd_hpk_45, v_hpk_45)
                guardar_txt(ruta+"/"+f_m.upper()+"_60.txt", f_e, media_espectro_60, "60", sd_hpk_60, v_hpk_60)
                guardar_txt(ruta+"/"+f_m.upper()+"_75.txt", f_e, media_espectro_75, "75", sd_hpk_75, v_hpk_75)
                guardar_txt(ruta+"/"+f_m.upper()+"_90.txt", f_e, media_espectro_90, "90", sd_hpk_90, v_hpk_90)
                
                tiempo_final_columns_8 = time() 
 
                tiempo_ejecucion_columns_8 = tiempo_final_columns_8 - tiempo_inicial_columns_8
 
                print ('El tiempo de ejecucion para hktable columns 8 fue:',tiempo_ejecucion_columns_8)
 
###############################################################################################################
# FORTH LOOP IN the monoenergetic tables for the ISO conversion coefficients at 8 incident angles: 0 -1800
# ("h_prime_3.csv", "h_prime_0.07.csv")
###############################################################################################################
        elif len(hk_table.columns) == 9:
            tiempo_inicial_columns_9 = time()
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MONOENERGÉTICO
            Ehk    = hk_table.iloc[:, 0].values
            hk_0   = hk_table.iloc[:, 1].values
            hk_15  = hk_table.iloc[:, 2].values
            hk_30  = hk_table.iloc[:, 3].values
            hk_45  = hk_table.iloc[:, 4].values
            hk_60  = hk_table.iloc[:, 5].values
            hk_75  = hk_table.iloc[:, 6].values
            hk_90  = hk_table.iloc[:, 7].values
            hk_180 = hk_table.iloc[:, 8].values
 
 
            # REALIZAR LOGARITMOS
            LEhk     = []
            Lhk_0    = []
            Lhk_15   = []
            Lhk_30   = []
            Lhk_45   = []
            Lhk_60   = []
            Lhk_75   = []
            Lhk_90   = []
            Lhk_180  = []
 
            for x in Ehk:
                LEhk.append(math.log(x))
 
            for x in hk_0:
                if x !=0:
                    Lhk_0.append(math.log(x))
                else:
                    Lhk_0.append(x)
 
            for x in hk_15:
                if x !=0:
                    Lhk_15.append(math.log(x))
                else:
                    Lhk_15.append(x)
 
            for x in hk_30:
                if x !=0:
                    Lhk_30.append(math.log(x))
                else:
                    Lhk_30.append(x)
 
            for x in hk_45:
                if x !=0:
                    Lhk_45.append(math.log(x))
                else:
                    Lhk_45.append(x)
 
            for x in hk_60:
                if x !=0:
                    Lhk_60.append(math.log(x))
                else:
                    Lhk_60.append(x)
 
            for x in hk_75:
                if x !=0:
                    Lhk_75.append(math.log(x))
                else:
                    Lhk_75.append(x)
 
            for x in hk_90:
                if x !=0:
                    Lhk_90.append(math.log(x))
                else:
                    Lhk_90.append(x)
 
            for x in hk_180:
                if x !=0:
                    Lhk_180.append(math.log(x))
                else:
                    Lhk_180.append(x)
 
 
 
            # LEER EL FICHERO MUTR_RHO  
            mutr_rho = pd.read_csv(var_mutrrho.get(), sep="\t", header=None, encoding='ISO-8859-1')
 
            # GUARDAR EN VARIABLES LOS VALORES DEL CSV MUTR_RHO
            E_mut_aux = mutr_rho.iloc[:, 0].values
            mtr_aux = mutr_rho.iloc[:, 1].values
 
            E_mut = []
            mtr = []
 
            # REEMPLAZAR LOS PUNTOS POR COMAS
            for x in E_mut_aux:
                    E_mut.append(float(x))
 
            for x in mtr_aux:
                    mtr.append(float(x))
 
            # REALIZAR LOS LOGARITMOS
            LE_mut = [math.log(x) for x in E_mut]
            Lmtr = [math.log(x) for x in mtr]
 
 
            # LEER EL FICHERO ESPECTROS
            for f_e in ficheros_espectros:
                espectro = pd.read_csv(directorio2.get()+"/"+f_e, sep=",")
 
 
                # GUARDAR EN VARIABLES LOS VALORES DEL CSV ESPECTROS
                E        = espectro.iloc[:, 0].values
                fluencia = espectro.iloc[:, 1].values
                kerma    = espectro.iloc[:, 2].values
                nfilas   = len(fluencia)
 
 
                # REALIZAR INTERPOLACIONES
                LE = []
                for x in E:
                    LE.append(math.log(x))
 
 
                # REALIZAR INTERPOLACIÓN CON MUTR_RHO
                interpolacion_uno_mut = interpolate.Akima1DInterpolator(LE_mut, Lmtr, axis=0)
                ln_p_int = []
 
                for i in LE:
                    interpolacion_final_mut = math.exp(interpolacion_uno_mut(i))
                    ln_p_int.append(interpolacion_final_mut)
 
                p_int = ln_p_int
 
 
                # REALIZAR INTERPOLACIÓN CON HK
                interpolacion_uno_0   = interpolate.Akima1DInterpolator(LEhk, Lhk_0, axis=0)
                interpolacion_uno_15  = interpolate.Akima1DInterpolator(LEhk, Lhk_15, axis=0)
                interpolacion_uno_30  = interpolate.Akima1DInterpolator(LEhk, Lhk_30, axis=0)
                interpolacion_uno_45  = interpolate.Akima1DInterpolator(LEhk, Lhk_45, axis=0)
                interpolacion_uno_60  = interpolate.Akima1DInterpolator(LEhk, Lhk_60, axis=0)
                interpolacion_uno_75  = interpolate.Akima1DInterpolator(LEhk, Lhk_75, axis=0)
                interpolacion_uno_90  = interpolate.Akima1DInterpolator(LEhk, Lhk_90, axis=0)
                interpolacion_uno_180 = interpolate.Akima1DInterpolator(LEhk, Lhk_180, axis=0)
 
                hk_int_0   = []
                hk_int_15  = []
                hk_int_30  = []
                hk_int_45  = []
                hk_int_60  = []
                hk_int_75  = []
                hk_int_90  = []
                hk_int_180 = []
 
                for i in LE:
                    interpolacion_final_0  = math.exp(interpolacion_uno_0(i))
                    hk_int_0.append(interpolacion_final_0)
 
                    interpolacion_final_15 = math.exp(interpolacion_uno_15(i))
                    hk_int_15.append(interpolacion_final_15)
 
                    interpolacion_final_30 = math.exp(interpolacion_uno_30(i))
                    hk_int_30.append(interpolacion_final_30)
 
                    interpolacion_final_45 = math.exp(interpolacion_uno_45(i))
                    hk_int_45.append(interpolacion_final_45)
 
                    interpolacion_final_60 = math.exp(interpolacion_uno_60(i))
                    hk_int_60.append(interpolacion_final_60)
 
                    interpolacion_final_75 = math.exp(interpolacion_uno_75(i))
                    hk_int_75.append(interpolacion_final_75)
 
                    interpolacion_final_90 = math.exp(interpolacion_uno_90(i))
                    hk_int_90.append(interpolacion_final_90)
 
                    interpolacion_final_180 = math.exp(interpolacion_uno_180(i))
                    hk_int_180.append(interpolacion_final_180)
 
 
 
                # DECLARAR MATRICES Y VECTORES
                Emat    = np.zeros((nfilas, n))
                flumat  = np.zeros((nfilas, n))
                mutrmat = np.zeros((nfilas, n))
 
                dhpk      = np.zeros(shape=n)
                nhpk_0    = np.zeros(shape=n)
                nhpk_15   = np.zeros(shape=n)
                nhpk_30   = np.zeros(shape=n)
                nhpk_45   = np.zeros(shape=n)
                nhpk_60   = np.zeros(shape=n)
                nhpk_75   = np.zeros(shape=n)
                nhpk_90   = np.zeros(shape=n)
                nhpk_180  = np.zeros(shape=n)
                hpk_0     = np.zeros(shape=n)
                hpk_15    = np.zeros(shape=n)
                hpk_30    = np.zeros(shape=n)
                hpk_45    = np.zeros(shape=n)
                hpk_60    = np.zeros(shape=n)
                hpk_75    = np.zeros(shape=n)
                hpk_90    = np.zeros(shape=n)
                hpk_180   = np.zeros(shape=n)
 
                for j in range(n):
                    nhpk_0[j]   = 0.0
                    nhpk_15[j]  = 0.0
                    nhpk_30[j]  = 0.0
                    nhpk_45[j]  = 0.0
                    nhpk_60[j]  = 0.0
                    nhpk_75[j]  = 0.0
                    nhpk_90[j]  = 0.0
                    nhpk_180[j] = 0.0
                    dhpk[j]     = 0.0
 
                    for i in range(nfilas):
                        Emat[i,j]    = np.random.normal(E[i], uEr*E[i], 1)
                        flumat[i,j]  = np.random.normal(fluencia[i], uflur*fluencia[i], 1)
                        mutrmat[i,j] = np.random.normal(p_int[i], umutrr*p_int[i], 1)
 
                        nhpk_0[j]   = nhpk_0[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_0[i])
                        nhpk_15[j]  = nhpk_15[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_15[i])
                        nhpk_30[j]  = nhpk_30[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_30[i])
                        nhpk_45[j]  = nhpk_45[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_45[i])
                        nhpk_60[j]  = nhpk_60[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_60[i])
                        nhpk_75[j]  = nhpk_75[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_75[i])
                        nhpk_90[j]  = nhpk_90[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_90[i])
                        nhpk_180[j] = nhpk_180[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j]*hk_int_180[i])
 
                        dhpk[j]    = dhpk[j]+ (Emat[i,j]*flumat[i,j]*mutrmat[i,j])
 
                        hpk_0[j]   = nhpk_0[j]/dhpk[j]
                        hpk_15[j]  = nhpk_15[j]/dhpk[j]
                        hpk_30[j]  = nhpk_30[j]/dhpk[j]
                        hpk_45[j]  = nhpk_45[j]/dhpk[j]
                        hpk_60[j]  = nhpk_60[j]/dhpk[j]
                        hpk_75[j]  = nhpk_75[j]/dhpk[j]
                        hpk_90[j]  = nhpk_90[j]/dhpk[j]
                        hpk_180[j] = nhpk_180[j]/dhpk[j]
 
                np.set_printoptions(linewidth=np.inf)
                print("")
                print("---------- ESPECTROS ANGULOS 180º ----------")     
 
 
                # MEDIA DEL ESPECTRO
                media_espectro_0 = statistics.mean(hpk_0)
                media_espectro_15 = statistics.mean(hpk_15)
                media_espectro_30 = statistics.mean(hpk_30)
                media_espectro_45 = statistics.mean(hpk_45)
                media_espectro_60 = statistics.mean(hpk_60)
                media_espectro_75 = statistics.mean(hpk_75)
                media_espectro_90 = statistics.mean(hpk_90)
                media_espectro_180 = statistics.mean(hpk_180)
                
                sd_hpk_0          = statistics.pstdev(hpk_0)
                sd_hpk_15         = statistics.pstdev(hpk_15)
                sd_hpk_30         = statistics.pstdev(hpk_30)
                sd_hpk_45         = statistics.pstdev(hpk_45)
                sd_hpk_60         = statistics.pstdev(hpk_60)
                sd_hpk_75         = statistics.pstdev(hpk_75)
                sd_hpk_90         = statistics.pstdev(hpk_90)
                sd_hpk_180         = statistics.pstdev(hpk_180)
                
                v_hpk_0           = sd_hpk_0*100/media_espectro_0
                v_hpk_15          = sd_hpk_15*100/media_espectro_15
                v_hpk_30          = sd_hpk_30*100/media_espectro_30
                v_hpk_45          = sd_hpk_45*100/media_espectro_45
                v_hpk_60          = sd_hpk_60*100/media_espectro_60
                v_hpk_75          = sd_hpk_75*100/media_espectro_75
                v_hpk_90          = sd_hpk_90*100/media_espectro_90
                v_hpk_180          = sd_hpk_180*100/media_espectro_180
                
                # plt.hist(hpk_0, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_0.pdf')
                #
                # plt.hist(hpk_15, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_15.pdf')
                #
                # plt.hist(hpk_30, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_30.pdf')
                #
                # plt.hist(hpk_45, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_45.pdf')
                #
                # plt.hist(hpk_60, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_60.pdf')
                #
                # plt.hist(hpk_75, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_75.pdf')
                #
                # plt.hist(hpk_90, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_90.pdf')
                #
                # plt.hist(hpk_180, 400, edgecolor="black", linewidth=1.2)
                # plt.show()
                # plt.savefig('HPK_180.pdf')
                #
                print("|Fichero monoenergético:",f_m)
                print("|Fichero espectro:",f_e)
                
                print("|Valor medio del espectro leído 0º:",media_espectro_0)
                print("|Valor medio del espectro leído 15º:",media_espectro_15)
                print("|Valor medio del espectro leído 30º:",media_espectro_30)
                print("|Valor medio del espectro leído 45º:",media_espectro_45)
                print("|Valor medio del espectro leído 60º:",media_espectro_60)
                print("|Valor medio del espectro leído 75º:",media_espectro_75)
                print("|Valor medio del espectro leído 75º:",media_espectro_90)
                print("|Valor medio del espectro leído 180º:",media_espectro_180)
                
                print("|Desviación del espectro 0º:",sd_hpk_0)
                print("|Desviación del espectro 15º:",sd_hpk_15)
                print("|Desviación del espectro 30º:",sd_hpk_30)
                print("|Desviación del espectro 45º:",sd_hpk_45)
                print("|Desviación del espectro 60º:",sd_hpk_60)
                print("|Desviación del espectro 75º:",sd_hpk_75)
                print("|Desviación del espectro 90º:",sd_hpk_90)
                print("|Desviación del espectro 180º:",sd_hpk_180)
                
                print("|V_HPK 0º:",v_hpk_0)
                print("|V_HPK 15º:",v_hpk_15)
                print("|V_HPK 30º:",v_hpk_30)
                print("|V_HPK 45º:",v_hpk_45)
                print("|V_HPK 60º:",v_hpk_60)
                print("|V_HPK 75º:",v_hpk_75)
                print("|V_HPK 90º:",v_hpk_90)
                print("|V_HPK 180º:",v_hpk_180)
 
                guardar_txt(ruta+"/"+f_m.upper()+"_0.txt", f_e, media_espectro_0, "0", sd_hpk_0, v_hpk_0)
                guardar_txt(ruta+"/"+f_m.upper()+"_15.txt", f_e, media_espectro_15, "15", sd_hpk_15, v_hpk_15)
                guardar_txt(ruta+"/"+f_m.upper()+"_30.txt", f_e, media_espectro_30, "30", sd_hpk_30, v_hpk_30)
                guardar_txt(ruta+"/"+f_m.upper()+"_45.txt", f_e, media_espectro_45, "45", sd_hpk_45, v_hpk_45)
                guardar_txt(ruta+"/"+f_m.upper()+"_60.txt", f_e, media_espectro_60, "60", sd_hpk_60, v_hpk_60)
                guardar_txt(ruta+"/"+f_m.upper()+"_75.txt", f_e, media_espectro_75, "75", sd_hpk_75, v_hpk_75)
                guardar_txt(ruta+"/"+f_m.upper()+"_90.txt", f_e, media_espectro_90, "90", sd_hpk_90, v_hpk_90)
                guardar_txt(ruta+"/"+f_m.upper()+"_180.txt", f_e, media_espectro_180, "180", sd_hpk_180, v_hpk_180)
                
                tiempo_final_columns_9 = time() 
 
                tiempo_ejecucion_columns_9 = tiempo_final_columns_9 - tiempo_inicial_columns_9
 
                print ('El tiempo de ejecucion para hktable columns 9 fue:',tiempo_ejecucion_columns_9)
                
 
 
pantalla.mainloop()