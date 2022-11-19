import sqlite3 as sqlite3
import barcodenumber
import re

connnection = sqlite3.connect('mis_datos3.db')
cursor = connnection.cursor()

miTupla = []
MiTupladePares = []


# Creamos la bd con los campos CABYS CODBAR IVA

cursor.execute('''CREATE TABLE IF NOT EXISTS
                  articulos (mi_index INTEGER PRIMARY KEY,
                  codbar VARCHAR(13),
                  cabys VARCHAR(13),
                  descripcion TEXT UNIQUE,
                  desccabys TEXT,
                  impuesto VARCHAR(3) )''')

def traeDescripcion(cabys):
    connnection = sqlite3.connect('cabys.db')
    cursor = connnection.cursor()

    cursor.execute(f'SELECT descripcion from articulos where cabys={cabys}')

    try:
        respuesta = cursor.fetchone()[0].replace('"', '')
    except:
        respuesta = "NADA"
    #print(repuesta)

    return respuesta

def traeImpuesto(cabys):
    connnection = sqlite3.connect('cabys.db')
    cursor = connnection.cursor()

    cursor.execute(f'SELECT impuesto from articulos where cabys={cabys}')

    try:
        respuesta = cursor.fetchone()[0]
    except:
        respuesta = "NADA"
    #print(repuesta)

    return respuesta



def miExtractor1(datos):
    tempLinea=''
    
    tempLinea = re.sub(r"\W"," ",datos) #reemplaza por espacios vacios lo que no sea caracter
    arrayLine = tempLinea.split() # genera un array separado poe espacios en blanco
    
    #recorre el array y realiza un append a tupla según las coicidencias
    for elemento in range(len(arrayLine)):
        if arrayLine[elemento]=="Codigo" and arrayLine[elemento+2]=="CodigoComercial" :
            miTupla.append(arrayLine[elemento+1].lower())
            miTupla.append(arrayLine[elemento+6].lower())
        elif arrayLine[elemento]=="Detalle": 
            miTupla.append(arrayLine[elemento+1].lower())

        #print("Tupla: ",miTupla)
    
    return miTupla

def armaPares(lista):
    for index in range(0,len(lista)-1,2):
        if barcodenumber.check_code('ean13',lista[index+1]):
            MiTupladePares.append([lista[index],lista[index+1]])
            
#all data contiene toda la informacón, data tiene menos registros para pruebas
            
with open ('allData.txt', encoding="utf8" ) as misDatos:
    for cadaLinea in misDatos:
        miExtractor1(cadaLinea)
        



for par in range(0,miTupla.__len__()-1,3):
    try:
        print(traeDescripcion(miTupla[par]))
        print(traeImpuesto(miTupla[par]))
        cursor.execute(f'''
            INSERT INTO articulos VALUES({par/3},
            "{miTupla[par]}",
            "{miTupla[par+1]}",
            "{miTupla[par+2]}",
            "{traeDescripcion(miTupla[par])}",
            "{traeImpuesto(miTupla[par])}")''')
        connnection.commit()
    except sqlite3.IntegrityError as e:
        None
        #print(e.args[0])

connnection.close()
    


