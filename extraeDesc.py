import re
import json
from operator import itemgetter

miTupla = []
MiTupladePares = []
miDictionary = {}

#funcion que comvierte en array las lineas de facturas electronicas y las carga en miTupla
def miExtractor1(datos):
    tempLinea=''
    
    tempLinea = re.sub(r"\W"," ",datos) #reemplaza por espacios vacios lo que no sea caracter
    arrayLine = tempLinea.split() # genera un array separado poe espacios en blanco
    
    #recorre el array y realiza un append a tupla según las coicidencias
    for elemento in range(len(arrayLine)):
        if arrayLine[elemento]=="Codigo" and arrayLine[elemento+2]=="CodigoComercial" :
            miTupla.append(arrayLine[elemento+1].lower())
        elif arrayLine[elemento]=="Detalle": 
            miTupla.append(arrayLine[elemento+1].lower())
    
    return miTupla

# Genera una lista de tuplas agregando de a dos elemento (codigo y articulos)
def armaPares(lista):
    for index in range(0,len(lista)-1,2):
        MiTupladePares.append([lista[index],lista[index+1]])

# Abre el archivo data.txt que contiene el extracto de FE y envia cada linea a miExtractor1
with open ('allData.txt', encoding="utf8" ) as misDatos:
    for cadaLinea in misDatos:
        miExtractor1(cadaLinea)

#Envia las mitupla para que se armen los pares 
armaPares(miTupla)

#Base de orden para las tupasl, index 0 (codigo)
baseOrden = itemgetter(0)

#ordena en base a baseOrden
MiTupladePares.sort(key=baseOrden)


#importamos groupby para agrupar items por codigo
from itertools import groupby

result = []

#por cada par codigo - item que esta el groupby agrega en forma de dict un elemento a result
for key, valuesiter in groupby(MiTupladePares, key=baseOrden):
    result.append(dict(type=key, items=list(v[1] for v in valuesiter)))

print(result)

#Dumps convierte el objeto python en un objeto JSON
tempDump = json.dumps(result)
transform = json.loads(tempDump)

print(transform)

with open('json_data.json', 'w') as outfile:
    json.dump(transform, outfile)