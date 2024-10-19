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
for s in range(1):  #semanas
    sublista = []
    num = []
    for c in range(1, 130):  #clientes
        if c in familia_2_valores:
            num.append(c)
        # Quiero un numero que sea 30% un valor y 70% de probabilidad otro valor
            if random.random() < 0.2: #NO SE ACTIVA NO VAMOS!!!
                sublista.append(random.randint(0,2311))
            else: #voyyyy
                sublista.append(random.randint(2312,2890))
        elif c in familia_3_valores:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 3466))
            else:
                sublista.append(random.randint(3467,4334))
        elif c in familia_4_valores:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 4622))
            else:
                sublista.append(random.randint(4623,5779))
        elif c in familia_5_valores:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 5778))
            else:
                sublista.append(random.randint(5779,7224))
        elif c == APR[1-1]:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 9999))
            else:
                sublista.append(random.randint(10000,12500))
        elif c == APR[2-1]:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 23999))
            else:
                sublista.append(random.randint(24000,30000))
        elif c == APR[3-1]:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 39999))
            else:
                sublista.append(random.randint(40000,50000))
        elif c == APR[4-1]:
            num.append(c)
            if random.random() < 0.2:
                sublista.append(random.randint(0, 7999))
            else:
                sublista.append(random.randint(8000,10000))
    demandas.append(sublista)
    num_total.append(num)
    



    # Agregar una columna indicando el número de semana y la demanda de cada cliente
    for num_total, demanda in enumerate(sublista):
        demandas_totales.append({"Semana": s+1,"Estanque": num_total+1, "Agua_inicial": demanda})

# Convertir a DataFrame
df_demandas = pd.DataFrame(demandas_totales)

# Guardar el DataFrame completo en una sola hoja de Excel
df_demandas.to_excel("agua_inicial.xlsx", index=False)
