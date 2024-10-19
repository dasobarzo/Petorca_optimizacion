import random
import pandas as pd

#Familias
grupos = {
    '2': 10,
    '3': 35,
    '4': 39,
    '5': 36,
    "APR":4,
    "CC":5
}

# Generar una lista de posiciones del 1 al 120
posiciones = list(range(1, 125))

random.shuffle(posiciones)

# Crear las listas para cada grupo
familias_2 = posiciones[:grupos['2']]
familias_3 = posiciones[grupos['2']:grupos['2'] + grupos['3']]
familias_4 = posiciones[grupos['2'] + grupos['3']:grupos['2'] + grupos['3'] + grupos['4']]
familias_5 = posiciones[grupos['2'] + grupos['3'] + grupos['4']:grupos['2'] + grupos['3'] + grupos['4'] + grupos['5']]
APR = posiciones[grupos['2'] + grupos['3'] + grupos['4'] + grupos['5']:grupos['2'] + grupos['3'] + grupos['4'] + grupos['5'] + grupos['APR']]
CC = [125,126,127,128,129]

#DataFrame
data = {
    'familias_2': pd.Series(familias_2),
    'familias_3': pd.Series(familias_3),
    'familias_4': pd.Series(familias_4),
    'familias_5': pd.Series(familias_5),
    "APR": pd.Series(APR),
    "CC": pd.Series(CC)
}

df = pd.DataFrame(data)

#Excel
df.to_excel('estanques_de_familias.xlsx', index=False)

