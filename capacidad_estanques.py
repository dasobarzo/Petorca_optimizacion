import random
import pandas as pd
from pandas import ExcelWriter

datos_familias = pd.read_excel("estanques_de_familias.xlsx", engine="openpyxl")

# Acceder a la columna 'familias_2' y convertirla en una lista
familia_2_valores = datos_familias['familias_2'].dropna().astype(int).tolist()
familia_3_valores = datos_familias['familias_3'].dropna().astype(int).tolist()
familia_4_valores = datos_familias['familias_4'].dropna().astype(int).tolist()
familia_5_valores = datos_familias['familias_5'].dropna().astype(int).tolist()
APR = datos_familias['APR'].dropna().astype(int).tolist()

# Mostrar los valores en la lista
#print(familia_2_valores)
demandas_totales = []
demandas = []
num_total=[]
for d in range(1):  #semanas
    sublista = []
    num = []
    for c in range(1, 130):  #clientes
        if c in familia_2_valores:
            sublista.append(2890)
        elif c in familia_3_valores:
            sublista.append(4334)
        elif c in familia_4_valores:
            sublista.append(5779)
        elif c in familia_5_valores:
            sublista.append(7224)
    demandas.append(sublista)    

    # Agregar una columna indicando el número de semana y la demanda de cada cliente
    for num_total, demanda in enumerate(sublista):
        demandas_totales.append({"Estanque": num_total+1, "Capacidad": demanda})

# Convertir a DataFrame
df_demandas = pd.DataFrame(demandas_totales)

# Guardar el DataFrame completo en una sola hoja de Excel
df_demandas.to_excel("capacidad_estanques.xlsx", index=False)