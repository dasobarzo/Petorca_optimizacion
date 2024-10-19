import pandas as pd
import numpy as np
import math
# Lista de coordenadas
coordenadas = [
    "32°12'15\"S 71°07'24\"W",
    "32°12'14\"S 71°07'18\"W",
    "32°12'13\"S 71°07'17\"W",
    "32°12'15\"S 71°07'15\"W",
    "32°12'02\"S 71°07'08\"W",
    "32°11'55\"S 71°06'55\"W",
    "32°11'28\"S 71°06'35\"W",
    "32°11'26\"S 71°06'36\"W",
    "32°11'24\"S 71°06'34\"W",
    "32°11'29\"S 71°06'42\"W",
    "32°11'25\"S 71°06'33\"W",
    "32°10'42\"S 71°05'16\"W",
    "32°10'33\"S 71°04'49\"W",
    "32°10'32\"S 71°04'48\"W",
    "32°10'19\"S 71°04'42\"W",
    "32°10'16\"S 71°04'29\"W",
    "32°13'49\"S 70°57'13\"W",
    "32°13'50\"S 70°57'15\"W",
    "32°13'49\"S 70°57'15\"W",
    "32°13'49\"S 70°57'15\"W",
    "32°13'50\"S 70°57'15\"W",
    "32°13'50\"S 70°57'15\"W",
    "32°12'47\"S 70°57'10\"W",
    "32°12'50\"S 70°57'13\"W",
    "32°12'48\"S 70°57'13\"W",
    "32°12'49\"S 70°57'13\"W",
    "32°12'44\"S 70°57'14\"W",
    "32°12'44\"S 70°57'13\"W",
    "32°12'39\"S 70°57'12\"W",
    "32°12'14\"S 70°57'15\"W",
    "32°12'14\"S 70°57'15\"W",
    "32°12'14\"S 70°57'12\"W",
    "32°12'10\"S 70°57'17\"W",
    "32°12'11\"S 70°57'17\"W",
    "32°12'06\"S 70°57'17\"W",
    "32°12'05\"S 70°57'16\"W",
    "32°12'12\"S 70°57'17\"W",
    "32°12'12\"S 70°57'17\"W",
    "32°14'01\"S 70°57'16\"W",
    "32°14'01\"S 70°57'16\"W",
    "32°14'00\"S 70°57'15\"W",
    "32°13'55\"S 70°57'19\"W",
    "32°13'55\"S 70°57'18\"W",
    "32°13'55\"S 70°57'18\"W",
    "32°13'50\"S 70°57'38\"W",
    "32°13'52\"S 70°58'12\"W",
    "32°13'53\"S 70°58'10\"W",
    "32°13'50\"S 70°58'13\"W",
    "32°13'52\"S 70°58'09\"W",
    "32°13'40\"S 70°58'35\"W",
    "32°13'36\"S 70°58'39\"W",
    "32°13'35\"S 70°58'42\"W",
    "32°13'34\"S 70°58'43\"W",
    "32°12'13\"S 70°57'14\"W",
    "32°12'13\"S 70°57'14\"W",
    "32°12'28\"S 70°57'11\"W",
    "32°12'57\"S 70°57'15\"W",
    "32°13'47\"S 70°57'17\"W",
    "32°13'47\"S 70°57'16\"W",
    "32°13'49\"S 70°57'17\"W",
    "32°13'49\"S 70°57'17\"W",
    "32°13'51\"S 70°57'17\"W",
    "32°13'51\"S 70°57'17\"W",
    "32°13'52\"S 70°57'16\"W",
    "32°13'50\"S 70°57'18\"W",
    "32°13'52\"S 70°57'18\"W",
    "32°13'52\"S 70°57'18\"W",
    "32°13'50\"S 70°57'18\"W",
    "32°13'51\"S 70°57'18\"W",
    "32°13'50\"S 70°57'17\"W",
    "32°13'50\"S 70°57'17\"W",
    "32°13'49\"S 70°57'17\"W",
    "32°13'48\"S 70°57'17\"W",
    "32°13'48\"S 70°57'17\"W",
    "32°13'49\"S 70°57'15\"W",
    "32°13'50\"S 70°57'15\"W",
    "32°13'50\"S 70°57'15\"W",
    "32°13'56\"S 70°57'17\"W",
    "32°13'57\"S 70°57'17\"W",
    "32°13'58\"S 70°57'19\"W",
    "32°10'08\"S 71°04'07\"W",
    "32°10'09\"S 71°04'06\"W",
    "32°10'09\"S 71°04'05\"W",
    "32°10'23\"S 71°03'45\"W",
    "32°10'20\"S 71°03'42\"W",
    "32°10'11\"S 71°03'46\"W",
    "32°10'16\"S 71°03'39\"W",
    "32°10'08\"S 71°02'56\"W",
    "32°09'48\"S 71°02'10\"W",
    "32°09'48\"S 71°02'10\"W",
    "32°09'48\"S 71°02'10\"W",
    "32°09'47\"S 71°02'09\"W",
    "32°09'36\"S 71°01'54\"W",
    "32°09'32\"S 71°01'52\"W",
    "32°08'53\"S 71°00'01\"W",
    "32°08'53\"S 70°59'59\"W",
    "32°08'53\"S 70°59'58\"W",
    "32°10'31\"S 71°04'48\"W",
    "32°10'31\"S 71°04'51\"W",
    "32°10'33\"S 71°04'55\"W",
    "32°10'34\"S 71°04'54\"W",
    "32°10'36\"S 71°04'59\"W",
    "32°10'41\"S 71°05'12\"W",
    "32°10'41\"S 71°05'13\"W",
    "32°10'41\"S 71°05'14\"W",
    "32°10'53\"S 71°05'57\"W",
    "32°10'54\"S 71°05'58\"W",
    "32°11'24\"S 71°06'35\"W",
    "32°11'45\"S 71°06'42\"W",
    "32°11'47\"S 71°06'42\"W",
    "32°11'58\"S 71°07'00\"W",
    "32°12'00\"S 71°07'03\"W",
    "32°12'14\"S 71°07'13\"W",
    "32°12'11\"S 71°07'15\"W",
    "32°12'11\"S 71°07'15\"W",
    "32°12'12\"S 71°07'15\"W",
    "32°12'20\"S 71°07'16\"W",
    "32°12'14\"S 71°07'13\"W",
    "32°12'14\"S 71°07'14\"W",
    "32°12'12\"S 71°07'13\"W",
    "32°10'48\"S 71°09'36\"W",
    "32°11'45\"S 71°07'57\"W",
    "32°13'02\"S 70°49'18\"W",
    "32°15'07\"S 70°56'48\"W",
    "32°16'45\"S 71°00'40\"W",
    "32°20'23\"S 71°04'26\"W",
    "32°11'50\"S 70°49'02\"W",
    "32°14'58\"S 70°53'03\"W",
    "32°15'25\"S 70°56'24\"W"
]

def dms_a_decimal(coordenada):
    latitud_dms, longitud_dms = coordenada.split(" ")
    
    def convertir_dms(dms):
        if '°' in dms and "'" in dms and '"' in dms:
            partes = dms.split("°")
            grados = float(partes[0])
            minutos_segundos = partes[1].strip().split("'")
            minutos = float(minutos_segundos[0])
            segundos_direccion = minutos_segundos[1].strip()
            segundos, direccion = segundos_direccion.split('"')

            segundos = float(segundos)

            decimal = grados + (minutos / 60) + (segundos / 3600)

            if direccion in ['S', 'W']:
                decimal = -decimal

            return decimal
        else:
            raise ValueError("El formato de la coordenada no es válido.")

    # Convertir las coordenadas
    latitud_decimal = convertir_dms(latitud_dms)
    longitud_decimal = convertir_dms(longitud_dms)

    return latitud_decimal, longitud_decimal

nodos = []
for i in coordenadas:
    latitud_decimal, longitud_decimal = dms_a_decimal(i)
    nodos.append([latitud_decimal,longitud_decimal])

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    #fórmula del Haversine
    a = np.add(np.power(np.sin(np.divide(dlat, 2)), 2),
               np.multiply(np.cos(lat1),
                           np.multiply(np.cos(lat2),
                                       np.power(np.sin(np.divide(dlon, 2)), 2))
                           )
              )
    c = np.multiply(2, np.arcsin(np.sqrt(a)))
    
    distance = R * c * 2
    return distance

distancias = []
for y in range(129):
    fila = []
    for x in range(129):
        latitud1 = nodos[x][0]
        longitud1 = nodos[x][1]
        latitud2 = nodos[y][0]
        longitud2 = nodos[y][1]
        distancia = haversine(latitud1, longitud1, latitud2, longitud2)
        fila.append(distancia)
    distancias.append(fila)

nombres_nodos = [f'Nodo {int(i)+1}' for i in range(129)]

df = pd.DataFrame(distancias, index=nombres_nodos, columns=nombres_nodos)

nombre_archivo = 'distancias_permanentes.xlsx'
df.to_excel(nombre_archivo, float_format="%.4f")
