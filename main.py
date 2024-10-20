from gurobipy import GRB, Model
from gurobipy import quicksum
from random import randint
import pandas as pd
import matplotlib.pyplot as plt
from time import time
from inventario import inventario_estanques
from pandas import ExcelWriter
inicio = time()

#conjuntos

A = range(125,130) #centro de carga de agua
C = range(1,50) #conjunto de camiones                                   ------------------>
P = range(121,125) #conjunto de APR
R = range(1,121) #conjunto de estanque
D = range(1,365) #dias * semana
V = range(1,14) #viajes
N = range(1, 130)
M = [(i, j) for i in N for j in N if i != j]  #grafos
DEl1 = [(a,j) for a in A for j in N if a!=j]  #deltaA+
DEl2 = [(j,a) for j in N for a in A if a!=j]  #deltaA-
DEl3 = [(r,j) for r in R for j in N if r!=j]  #deltaR+
DEl4 = [(j,r) for j in N for r in R if r!=j]  #deltaR-
DEl5 = [(p,j) for p in P for j in N if p!=j]  #deltaP+
DEl1 = [(j,p) for j in N for p in P if p!=j]  #deltaP-






#datas
# Demanda exportada del excel al azar
datos_demanda_diaria = pd.read_excel("demanda_diaria.xlsx", engine="openpyxl")
datos_distancia = pd.read_excel("distancias_permanentes.xlsx", engine="openpyxl")
datos_estanques_familias = pd.read_excel("estanques_de_familias.xlsx", engine="openpyxl")

agua_por_tipo_de_estanque = [2890,4334,5779,7224]






#Definición de parámetros
# Distancias en kilómetros
L_m = {
    i+1: {j: valor for j, valor in enumerate(fila)} 
    for i, fila in datos_distancia.iterrows()}
print(L_m[1][2])


# Capacidades
K_c = 15000 # Capacidad del camión c en litros
DE_rd = {
    i+1: {j: valor for j, valor in enumerate(fila)} 
    for i, fila in datos_demanda_diaria.iterrows()
} # Demanda de agua en el estanque r en la semana s ------------------    aqui agregue d
AIE_r1 = 0
AIA_p1 = 0
DA_pd = {
    i+1: {j: valor for j, valor in enumerate(fila)} 
    for i, fila in datos_demanda_diaria.iterrows()
}# Demanda de agua en el APR p en la semana s---------------


# Presupuestos y almacenamiento
presupuesto_por_dia = 15566072 /7
KE_r =  [2890,4334,5779,7224]# Capacidad del estanque r en litros --------------------
KA_p = [12500, 30000, 50000, 10000]# Capacidad del APR p en litros --------------------
O_as =  [120000/7,120000/7,120000/7,120000/7,120000/7] # Oferta de agua en el centro a en la semana s --------------------

# Sueldos y costos
lmbda = 162500 # Sueldo del camionero en CLP 
CD = 1035 # Costo por litro de combustible diesel
CPL = 100/40 # Autonomía, kms recorridos por litro de combustible en un camión aljíbe

PA_a = [17.31, 10.871, 11.444, 5.541, 17.697] # Costo por litro de agua en un centro a

# Modelo vacio 
model = Model()

# Variables de decision 
# x_csdr si el camion c se va a llenar al centro a en la semana s el día d
X = model.addVars(C, A, D, vtype=GRB.BINARY, name="x_csdr")
# y_csdr si el camion c en el dia d de la semana s va a llenar agua al estanque r
Y = model.addVars(C, D, R, vtype=GRB.BINARY, name="y_csdr")
# z_csdp si el camión c en el dia d de la semana s va a llenar agua al APR p
Z = model.addVars(C, D, P, vtype=GRB.BINARY, name="z_csdp")
# lc_casd litros de agua cargados al camion c en el centro a en la semana s del dia d
LC = model.addVars(C, A, D, vtype=GRB.CONTINUOUS, name="lc_casd")
# le_csdr agua entregada en litros por el camion c en la semana s del dia d al estanque r
LE = model.addVars(C, D, R, vtype=GRB.CONTINUOUS, name="le_csdr")
# lea_csdp agua entregada en litros por el camion c en la semana s del dia d al APR p
LEA = model.addVars(C, D, P, vtype=GRB.CONTINUOUS, name="lea_csdp")
# kr_rd si el sensor del estanque r se enciende en el dia d
Kr = model.addVars(R, D, vtype=GRB.BINARY, name="kr_rd")
# kp_pd si el sensor del APR p se enciende en el dia d
Kp = model.addVars(P, D, vtype=GRB.BINARY, name="kp_pd")
# cf_cds si el camion c funciona en el dia d de la semana s
CF = model.addVars(C, D, vtype=GRB.BINARY, name="cf")
# u_cmd si el camion c utiliza el arco (i,j) en el dia d
U = model.addVars(C, M, D, vtype=GRB.BINARY, name="u_cmd")

model.update()

# Restricciones


#1,Cada camion c ∈ C debe ir a recargar APR p ∈ P y estanque r ∈ R como maximo 6 veces en un día d ∈ D.
model.addConstrs(((quicksum(Y[c,d,r] for r in R)+quicksum(Z[c,d,p] for p in P)) <= 6 for c in C for d in D), name = "R1") #revisar subindice s
'''
#2. Para transportar agua debe haber un camion c ∈ C disponible para hacerlo.
model.addConstrs((X[c,a,d]+Y[c,d,r]+Z[c,d,p] <= 1 for c in C), name ="R2") #que hacemos con los subindices????

#3.-
model.addConstrs((quicksum(DE_rd[d, r] for d in D) <= quicksum(quicksum(LE[c, d, r] for c in C) for d in D) for r in R), name="R3.1")
model.addConstrs((quicksum(DA_pd[d, p] for d in D) <= quicksum(quicksum(LEA[c, d, p] for c in C) for d in D) for p in P), name="R3.2")
#4.-
model.addConstrs((quicksum(quicksum(LC[c, a, d] for c in C) for d in D) <= O_as[a, d]for a in A for d in D), name="R4")
#5.-
model.addConstrs((quicksum(LC[c, a, d] for a in A) == quicksum(LE[c, d, r] for r in R) + quicksum(LEA[c, d, p] for p in P)for c in C for d in D),name="R5")
#6.-
model.addConstrs((LC[a, c, d] <= K[c] * X[c, a, d] for c in C for a in A for d in D),name="R6")
#7.
model.addConstrs((Kr[r, d, s] == Y[c, d + 1, r]for c in C for r in R for d in range(1, 7) for s in S),name="R7")
model.addConstrs((Kr[r, 7, s] == Y[c, 1, r]for c in C for r in R for s in S if s + 1 <= len(S)),name="R7.1")
model.addConstrs((quicksum(Kr[r, d, s] for d in D) <= 1 for r in R for s in S),name="R7.2")
#8.-
model.addConstrs((Kp[p, d, s] == Z[c d + 1, p] for c in C for p in P for d in range(1, 7) for s in S),name="R8.1")
model.addConstrs((Kp[p, 7, s] == Z[c, 1, p] for c in C for p in P for s in S),name="R8.2")
#9.-
model.addConstrs((Kr[r, d] == CF[c, d] for c in C for d in D for r in R),name="R9")
#10.-
model.addConstrs((LE[c, d, r] <= K_c * Y[c, d, r] for c in C for r in R for d in D),name="R10.1")
model.addConstrs((LEA[c, d, p] <= K_c * Z[c, d, p] for c in C for p in P for d in D),name="R10.2")
#11.-
model.addConstrs((quicksum(Y[c, d, r] for c in C for d in D) <= 1 for r in R),name="R11")

#12.-
model.addConstrs((quicksum(U[c, m, d, v] for m in REVISAR) == CF[c, d, s] for c in C for d in D for s in S for v in V),name="R12")
#13.-


model.addConstrs((quicksum(U[c, m, d, v] for m in nodos entrada) == Y[c, s, d, r] for c in C for m in revisar for d in D for s in S for r in R),name="R13.1")
model.addConstrs((quicksum(U[c, m, d, v] for m in nodos entrada) == Z[c, s, d, p] for c in C for m in revisar for d in D for s in S for p in P),name="R13.2")
#14.-
model.addConstrs((quicksum(U[c, m, d, v] for m in nodos salida) == Y[c, s, d, r] for c in C for m in N if m != A for d in D for s in S for r in R),name="R14.1")
model.addConstrs((quicksum(U[c, m, d, v] for m in nodos salida) == Z[c, s, d, p] for c in C for m in N if m != A for d in D for s in S for p in P),name="R14.2")
'''
model.update()
# Optimizar el modelo

#función objetivo
obj = quicksum(
    quicksum(
        (CD / CPL) * (                                                                                                            #------>
            quicksum(L_m[i][j] * U[c, i, j, d] for i, j in M for d in D) +  # Descomponer `m` en `i, j`
            quicksum(LC[c, a, d] * PA_a[a] for a in A for d in D)   # Litros cargados y costo por agua
        ) + 2 * lmbda for c in C))  # Cierra la suma por cada semana



# Definir la función objetivo
model.setObjective(obj, GRB.MINIMIZE)
model.optimize()


'''
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
'''

