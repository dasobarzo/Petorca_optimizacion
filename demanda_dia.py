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
datos_demanda_inicial = pd.read_excel("agua_inicial.xlsx", engine="openpyxl")

demandas_totales = []
demandas = []
demanda_semanal = [2890,4334,5779,7224]


for d in range(1,(7*52)+1): #dia

    sublista = []
    for c in range(1, 125):  #clientes
        if c in familia_2_valores:
        # Quiero un numero que sea 30% un valor y 70% de probabilidad otro valor
            if random.random() < 0.1: #NO SE ACTIVA NO VAMOS!!!
                n=2311//7
                sublista.append(random.randint(0,n))
            else: #voyyyy
                n=2312//7
                m = 2890//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(2312,2890/7))
        elif c in familia_3_valores:
            if random.random() < 0.1:
                n=3466//7
                sublista.append(random.randint(0, n))
            else:
                n=3467//7
                m = 4334//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(3467/7,4334/7))
        elif c in familia_4_valores:
            if random.random() < 0.1:
                n=4622//7
                sublista.append(random.randint(0, n))
            else:
                n=4623//7
                m = 5779//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(4623/7,5779/7))
        elif c in familia_5_valores:
            if random.random() < 0.1:
                n=5778//7
                sublista.append(random.randint(0, n))
            else:
                n=5779//7
                m = 7224//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(5779/7,7224/7))
        elif c == APR[1-1]:
            if random.random() < 0.1:
                n=9999//7
                sublista.append(random.randint(0, n))
            else:
                n=10000//7
                m =12500//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(10000/7,12500/7))
        elif c == APR[2-1]:
            if random.random() < 0.1:
                n=23999//7
                sublista.append(random.randint(0, n))
            else:
                n=24000//7
                m = 30000//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(24000/7,30000/7))
        elif c == APR[3-1]:
            if random.random() < 0.1:
                n=39999//7
                sublista.append(random.randint(0, n))
            else:
                n=4000//7
                m = 5000//7
                sublista.append(random.randint(n,m))
                #sublista.append(random.randint(40000,50000))
        elif c == APR[4-1]:
            if random.random() < 0.1:
                n=7999//7
                sublista.append(random.randint(0, n))
            else:
                n=8000//7
                m = 10000//7
                sublista.append(random.randint(n,m))
    
    demandas_totales.append(sublista)


# Guardar los resultados en un archivo Excel
nombres_nodos = [f'{i + 1}' for i in range(124)]

# Crear el DataFrame y definir el índice de 1 a 364
df = pd.DataFrame(demandas_totales, columns=nombres_nodos, index=range(1, 365))

# Guardar los resultados en un archivo Excel
nombre_archivo = 'demanda_diaria.xlsx'
df.to_excel(nombre_archivo, float_format="%.4f")