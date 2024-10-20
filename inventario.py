import pandas as pd
from pandas import ExcelWriter


# Cargar los datos desde el archivo Excel
datos_familias = pd.read_excel("agua_inicial.xlsx", engine="openpyxl")

# Crear la lista de listas con la columna 'Agua_inicial'
inventario_estanques = [[datos_familias["Agua_inicial"][i]] for i in range(len(datos_familias))]
print(inventario_estanques)

