import sqlite3 as sqlite3
import barcodenumber
import re

connnection = sqlite3.connect('mis_datos.db')
cursor = connnection.cursor()

miTupla = []
MiTupladePares = []

cursor.execute('''CREATE TABLE IF NOT EXISTS
                  articulos (mi_index INTEGER PRIMARY KEY,
                  codbar VARCHAR(13),
                  descripcion TEXT UNIQUE) ''')

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

def armaPares(lista):
    for index in range(0,len(lista)-1,2):
        if barcodenumber.check_code('ean13',lista[index+1]):
            MiTupladePares.append([lista[index],lista[index+1]])
            
            
with open ('allData.txt', encoding="utf8" ) as misDatos:
    for cadaLinea in misDatos:
        miExtractor1(cadaLinea)
        



print(miTupla.__len__())
print(miTupla[0])
print(miTupla[1])

for par in range(0,miTupla.__len__()-1,2):
    try:
        cursor.execute(f'INSERT INTO articulos VALUES({par/2},"{miTupla[par]}","{miTupla[par+1]}")')
        connnection.commit()
    except sqlite3.IntegrityError as e:
        None
        #print(e.args[0])

connnection.close()
    


