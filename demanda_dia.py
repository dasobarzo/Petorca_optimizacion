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
for s in range(52):  #semanas

    for d in range(7): #dia

        sublista = []
        for c in range(1, 125):  #clientes
            if c in familia_2_valores:
            # Quiero un numero que sea 30% un valor y 70% de probabilidad otro valor
                if random.random() < 0.2: #NO SE ACTIVA NO VAMOS!!!
                    n=2311//7
                    sublista.append(random.randint(0,n))
                else: #voyyyy
                    n=2312//7
                    m = 2890//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(2312,2890/7))
            elif c in familia_3_valores:
                if random.random() < 0.2:
                    n=3466//7
                    sublista.append(random.randint(0, n))
                else:
                    n=3467//7
                    m = 4334//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(3467/7,4334/7))
            elif c in familia_4_valores:
                if random.random() < 0.2:
                    n=4622//7
                    sublista.append(random.randint(0, n))
                else:
                    n=4623//7
                    m = 5779//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(4623/7,5779/7))
            elif c in familia_5_valores:
                if random.random() < 0.2:
                    n=5778//7
                    sublista.append(random.randint(0, n))
                else:
                    n=5779//7
                    m = 7224//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(5779/7,7224/7))
            elif c == APR[1-1]:
                if random.random() < 0.2:
                    n=9999//7
                    sublista.append(random.randint(0, n))
                else:
                    n=10000//7
                    m =12500//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(10000/7,12500/7))
            elif c == APR[2-1]:
                if random.random() < 0.2:
                    n=23999//7
                    sublista.append(random.randint(0, n))
                else:
                    n=24000//7
                    m = 30000//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(24000/7,30000/7))
            elif c == APR[3-1]:
                if random.random() < 0.2:
                    n=39999//7
                    sublista.append(random.randint(0, n))
                else:
                    n=4000//7
                    m = 5000//7
                    sublista.append(random.randint(n,m))
                    #sublista.append(random.randint(40000,50000))
            elif c == APR[4-1]:
                if random.random() < 0.2:
                    n=7999//7
                    sublista.append(random.randint(0, n))
                else:
                    n=8000//7
                    m = 10000//7
                    sublista.append(random.randint(n,m))
        
        demandas.append(sublista)



    # Agregar una columna indicando el número de semana y la demanda de cada cliente
        for idx, demanda in enumerate(sublista):
            demandas_totales.append({"Semana": s+1, "dia": d+1,"Estanque": idx+1, "Consumo": demanda})

# Convertir a DataFrame
df_demandas = pd.DataFrame(demandas_totales)

# Guardar el DataFrame completo en una sola hoja de Excel
df_demandas.to_excel("demandas_diaria.xlsx", index=False)