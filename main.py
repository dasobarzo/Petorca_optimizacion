from gurobipy import GRB, Model
from gurobipy import quicksum
from random import randint
import pandas as pd
import matplotlib.pyplot as plt
from time import time
inicio = time()

# definimos data: conjuntos y data 

A = range(1,5) #centro de carga de agua
C = range(1,4) #conjunto de camiones
P = range(1,4) #conjunto de APR
R = range(1,120) #conjunto de estanques
S = range(1,52) #tiempo en semanas
D = range(1,7) #dias de semana

# Demanda exportada del excel al azar
datos_demanda = pd.read_excel("Resultados_demanda.xlsx", engine="openpyxl")
datos_distancia = pd.read_excel("Resultados_distancia.xlsx", engine="openpyxl")

# Demanda exportada del excel al azar
datos_demanda = pd.read_excel("Resultados_demanda_por_tipo_de_hormigon.xlsx", engine="openpyxl")
datos_distancia = pd.read_excel("Resultados_distancia_por_tipo_hormigon.xlsx", engine="openpyxl")

presupuesto_por_dia = ((37500 * 40) + (4*22*2*114)*40 + (4*22*2*455)*0)
agua_por_tipo_de_estanque = [10000, 15000, 0.12046]

#Definición de parámetros
# Distancias en kilómetros
L_m1 = # Distancia entre estanques r1 y r2
L_m2 =  # Distancia entre un estanque y un APR
L_m3 = # Distancia entre un estanque y un centro de carga
L_m4 =   # Distancia entre dos APRs
L_m5 =  # Distancia entre un APR y un centro de carga
L_m6 =  # Distancia entre centros de carga

# Capacidades
K_c = 15000 # Capacidad del camión c en litros
DE_rs = # Demanda de agua en el estanque r en la semana s
DA_psd =  # Demanda de agua en el APR p en la semana s

# Presupuestos y almacenamiento
PT_s =   # Presupuesto en la semana s
KE_r =  # Capacidad del estanque r en litros
KA_p = # Capacidad del APR p en litros
O_as =  # Oferta de agua en el centro a en la semana s

# Sueldos y costos
Z = 162500 # Sueldo del camionero en CLP
CPL = # Costo por litro de diésel por kilómetro del camión ajíbe
CD = # Costo por litro de camión eléctrico por kilómetro
PA_a = 1040/1000 # Costo por litro de agua en un centro a

# Modelo vacio 
model = Model()

# Variables de decision 
x = model.addVars(R, C, T, S, vtype = GRB.BINARY, name = "x_rcts") # 1 si el camión eléctrico es usado el día t en la semana s por el cliente c, con c  C,  t  T,  s  S ; 0 EOC
y = model.addVars(Q, C, T, S, vtype = GRB.BINARY, name = "y_qcts") # 1 si el camión diesel es usado el día t en la semana s por el cliente c, con c  C,  t  T,  s  S;  0 EOC
zx = model.addVars(C, R, T, X, S, vtype = GRB.INTEGER, name = "zx_rtxs") # Cantidad de kilogramos de hormigón de tipo x transportado por  el camión eléctrico q en el día t en la semana s, con t  T, x  X, s  S
zy = model.addVars(C, Q, T, X, S, vtype = GRB.INTEGER, name = "zy_qtxs") # Cantidad de kilogramos de hormigón de tipo x transportado por camiones diésel en el día t en la semana s, con t  T, x  X, s  S
wx = model.addVars(C, R, T, X, S, vtype = GRB.BINARY, name = "wx_crtxs") # 1 si el camión eléctrico r transporta hormigón de tipo x el día t de la semana s hacia el cliente c, 0 EOC.
wy = model.addVars(C, Q, T, X, S, vtype = GRB.BINARY, name = "wx_cqtxs") # 1 si el camión diésel q transporta hormigón de tipo x el día t de la semana s hacia el cliente c, 0 EOC.


# Update
model.update()

# Restricciones











######################### NO TOCAR ANTIGUOOOOOOOOOO ##################################

# Demanda exportada del excel al azar
datos_demanda = pd.read_excel("Resultados_demanda.xlsx", engine="openpyxl")
datos_distancia = pd.read_excel("Resultados_distancia.xlsx", engine="openpyxl")


presupuesto_por_dia = ((37500 * 40) + (4*22*2*114)*40 + (4*22*2*455)*0)
contaminacion_tipo_hormigon = [0.05979, 0.082167, 0.12046]

# Demanda exportada del excel al azar
datos_demanda = pd.read_excel("Resultados_demanda_por_tipo_de_hormigon.xlsx", engine="openpyxl")
datos_distancia = pd.read_excel("Resultados_distancia_por_tipo_hormigon.xlsx", engine="openpyxl")



# Definimos los parametros
k = {c: 1 for c in C} # Distancia en kilómetros desde la planta hasta el cliente c, con c  C
a = 30000 # Paga al conductor si es día hábil en CLP
b = 45000 # Paga al conductor si es fin de semana en CLP
p = presupuesto_por_dia # Presupuesto en CLP del dia t en la semana s, con t  T, s  S. 
d = {(c, s, x1): 40000 for c in C for s in S for x1 in X} # Demanda en kilogramos de hormigón el dia t en la semana s, con t  T, s  S.
e = {x1: contaminacion_tipo_hormigon[x1-1] for x1 in X} # Emisiones dependiendo del tipo de hormigón x, de kg de CO2 por kg de hormigón. 
u = 0.592064 # Kilogramos de CO2 emitidos por kilómetro recorrido por camión diesel.
v = 0.5032544 # Kilogramos de CO2 emitidos por kilómetro recorrido, por camión eléctrico   
l = 114 # Gasto por kilómetro de un camión eléctrico en CLP. 
o = 455 # Gasto por kilómetro de un camión diesel en CLP.
S_t = {t: 1 if t <= 5 else 0 for t in T} # 1 si es día hábil, 0 e.o.c (fin de semana)
m = 30000 #big M

for index, row in datos_demanda.iterrows():
    s = row['Semana']
    c = row['Cliente']
    d[c, s, 1] = row['HGHD']
    d[c, s, 2] = row['HG5']
    d[c, s, 3] = row['H40']

for index, row in datos_distancia.iterrows():
    c = row['Cliente']
    k[c] = row['Distancia']




# Modelo vacio 
model = Model()

# Variables de decision 
x = model.addVars(R, C, T, S, vtype = GRB.BINARY, name = "x_rcts") # 1 si el camión eléctrico es usado el día t en la semana s por el cliente c, con c  C,  t  T,  s  S ; 0 EOC
y = model.addVars(Q, C, T, S, vtype = GRB.BINARY, name = "y_qcts") # 1 si el camión diesel es usado el día t en la semana s por el cliente c, con c  C,  t  T,  s  S;  0 EOC
zx = model.addVars(C, R, T, X, S, vtype = GRB.INTEGER, name = "zx_rtxs") # Cantidad de kilogramos de hormigón de tipo x transportado por  el camión eléctrico q en el día t en la semana s, con t  T, x  X, s  S
zy = model.addVars(C, Q, T, X, S, vtype = GRB.INTEGER, name = "zy_qtxs") # Cantidad de kilogramos de hormigón de tipo x transportado por camiones diésel en el día t en la semana s, con t  T, x  X, s  S
wx = model.addVars(C, R, T, X, S, vtype = GRB.BINARY, name = "wx_crtxs") # 1 si el camión eléctrico r transporta hormigón de tipo x el día t de la semana s hacia el cliente c, 0 EOC.
wy = model.addVars(C, Q, T, X, S, vtype = GRB.BINARY, name = "wx_cqtxs") # 1 si el camión diésel q transporta hormigón de tipo x el día t de la semana s hacia el cliente c, 0 EOC.


# Update
model.update()

# Restricciones 
# 1 La suma de los pagos al chofer y el costo por kilómetro avanzado deben ser menores al presupuesto diario.
model.addConstrs((p >= quicksum(((S_t[t]*a+(1-S_t[t])*b)*quicksum(x[r,c,t,s] for r in R) + 
                                 (S_t[t]*a+(1-S_t[t])*b) * quicksum(y[q,c,t,s] for q in Q) + 
                                 k[c]*l*quicksum(x[r,c,t,s] for r in R) + 
                                 k[c]*o*quicksum(y[q,c,t,s] for q in Q))for c in C) for t in T for s in S), name = "R1")

#2 Cada conductor de camión diésel debe trabajar máximo 4 veces al día.
model.addConstrs((quicksum(y[q,c,t,s] for c in C) <= 4 for q in Q for t in T for s in S), name = "R2")

#3 Cada conductor de camión eléctrico debe trabajar máximo 4 veces al día
model.addConstrs((quicksum(x[r,c,t,s] for c in C) <= 4 for r in R for t in T for s in S), name = "R3")

#4 La demanda de hormigón, no puede superar a la oferta producida.
model.addConstrs((quicksum((quicksum(zx[c,r,t,x1,s] for r in R) + 
                            quicksum(zy[c,q,t,x1,s] for q in Q))for t in T) >= d[c,s,x1] for x1 in X for s in S for c in C), name = "R4")

#5 La cantidad de hormigón transportado por un camión diésel, no puede superar su capacidad de transporte.
model.addConstrs((zy[c, q, t, x1, s] <= 28000 for q in Q for c in C for t in T for x1 in X for s in S), name = "R5")

#6 La cantidad de hormigón transportado por un camión eléctrico, no puede superar su capacidad de transporte.
model.addConstrs((zx[c, r, t, x1, s] <= 28000 for r in R for c in C for t in T for x1 in X for s in S), name = "R6")

#7a Para transportar una carga debe haber un camión disponible para hacerlo.
model.addConstrs((quicksum(zx[c,r,t,x1,s] for x1 in X) <= x[r,c,t,s] * m for c in C for r in R for t in T for s in S), name = "R7a")

#7b Para transportar una carga debe haber un camión disponible para hacerlo.
model.addConstrs((quicksum(zy[c,q,t,x1,s] for x1 in X) <= y[q,c,t,s] * m for c in C for q in Q for t in T for s in S), name = "R7b")

#8a Cada camión sólo puede transportar un tipo de cemento
model.addConstrs((quicksum(wx[c, r, t, x1, s] for x1 in X) <= x[r,c,t,s] for r in R for c in C for t in T for s in S), name = "R8a")

#8b Cada camión sólo puede transportar un tipo de cemento
model.addConstrs((quicksum(wy[c, q, t, x1, s] for x1 in X) <= y[q,c,t,s] for q in Q for c in C for t in T for s in S), name = "R8b")

# Funcion objetivo
objetivo = quicksum(quicksum(
    2 * (
        quicksum(x[r, c, t, s] * k[c] * v for r in R) + quicksum(y[q, c, t, s] * k[c] * u for q in Q))
    + quicksum((
            quicksum(zx[c, r, t, x1, s] for r in R) +
            quicksum(zy[c, q, t, x1, s] for q in Q)) * e[x1] for x1 in X
        ) for c in C )for t in T for s in S
)

model.setObjective(objetivo, GRB.MINIMIZE)

# Optimiza tu problema 
model.optimize()



# Contar el número total de camiones eléctricos utilizados durante el año
total_camiones_electricos = sum(x[r, c, t, s].x for r in R for c in C for t in T for s in S)

# Contar el número total de camiones diésel utilizados durante el año
total_camiones_diesel = sum(y[q, c, t, s].x for q in Q for c in C for t in T for s in S)

# Calculo de la contaminacion semanal de cada tipo de camion
contaminacion_electricos_semana = []
contaminacion_diesel_semana = []
for s in S:
    contaminacion_electricos = sum(x[r, c, t, s].X * k[c] * v for r in R for c in C for t in T) + \
                               sum(zx[c, r, t, x1, s].X * e[x1] for r in R for c in C for t in T for x1 in X)
    contaminacion_diesel = sum(y[q, c, t, s].X * k[c] * u for q in Q for c in C for t in T) + \
                           sum(zy[c, q, t, x1, s].X * e[x1] for q in Q for c in C for t in T for x1 in X)
    contaminacion_electricos_semana.append(contaminacion_electricos)
    contaminacion_diesel_semana.append(contaminacion_diesel)


final = time()
duracion_segundos = round(final - inicio)
duracion_minutos = round(duracion_segundos/60,1)

print(f"Total de camiones eléctricos utilizados durante el año: {total_camiones_electricos}")
print(f"Total de camiones diésel utilizados durante el año: {total_camiones_diesel}")

print(f"El programa se demoro {duracion_segundos} segundos")
print(f"El programa se demoro {duracion_minutos} minutos")



# Todo lo que esta despues de esta linea, es la iformacion que utilizamos dentro de excel 
# la dejamops como comntarios para que no se cambie la informacion


#df = pd.DataFrame({
#    'Semana': [i+1 for i in range(len(S))], 
#    'Contaminacion Electricos': contaminacion_electricos_semana, 
#    'Contaminacion Diesel': contaminacion_diesel_semana
#})

# Guardar el DataFrame en un archivo Excel
#df.to_excel("Resultado_contaminacion_semana.xlsx", index=False, engine='openpyxl')


# 1. Extracción de datos post-optimización
#resultados_electricos = {(c,x1): sum(zx[c,r,t,x1,s].x for r in R for t in T for s in S) for c in C for x1 in X}
#resultados_diesel = {(c,x1): sum(zy[c,q,t,x1,s].x for q in Q for t in T for s in S) for c in C for x1 in X}

# 2. Preparación de los datos
#df_electricos = pd.DataFrame(resultados_electricos, index=["Electricos"]).T
#df_diesel = pd.DataFrame(resultados_diesel, index=["Diesel"]).T

# 3. Guardar en Excel
#with pd.ExcelWriter('resultados_hormigon_transportado.xlsx') as writer:
#    df_electricos.to_excel(writer, sheet_name='Electricos')
#    df_diesel.to_excel(writer, sheet_name='Diesel')