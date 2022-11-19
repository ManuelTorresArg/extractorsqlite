import re
import json
import barcodenumber
from operator import itemgetter
import sqlite3 as sqlite3


connnection = sqlite3.connect('mis_datos4.db')
cursor = connnection.cursor()


# Creamos la bd con los campos CABYS CODBAR IVA

cursor.execute('''CREATE TABLE IF NOT EXISTS
                  articulos (cabys VARCHAR(13),
                  codbar VARCHAR(13),
                  descripcion TEXT UNIQUE) ''')

def generaRegistro(cabys, codbar, descripcion):
    if len(codbar) == 13:
        try:
            cursor.execute(f'INSERT INTO articulos VALUES({cabys},"{codbar}","{descripcion}")')
            connnection.commit()
        except sqlite3.IntegrityError as e:
            None
            #print(e.args[0])
        
        
        
def miExtractor1(datos):
    tempLinea=''
    
    tempLinea = re.sub(r"\W"," ",datos) #reemplaza por espacios vacios lo que no sea caracter
    arrayLine = tempLinea.split() # genera un array separado poe espacios en blanco
    
    #recorre el array y realiza un append a tupla según las coicidencias
    
    codigo = ""
    desc = ""
    cabys = ""
    
    
    for elemento in range(len(arrayLine)):
        if arrayLine[elemento]=="Codigo" and arrayLine[elemento+2]=="CodigoComercial" :
           cabys= (arrayLine[elemento+1].lower() if len(arrayLine[elemento+1].lower()) > 0 else "vacio")
        elif arrayLine[elemento]=="Codigo" and arrayLine[elemento+2]=="Cantidad" : 
            codigo = (arrayLine[elemento+1].lower() if len(arrayLine[elemento+1]) > 0 else "vacio")
        elif arrayLine[elemento]=="Detalle": 
            desc = (arrayLine[elemento+1].upper() if len(arrayLine[elemento+1]) > 0 else "vacio")
            
        if len(codigo) != 0 and len(desc) != 0 and len(cabys) != 0:
            generaRegistro(cabys, codigo, desc)
            codigo = ""
            desc = ""
            cabys = ""
            
           
        
# Abre el archivo data.txt que contiene el extracto de FE y envia cada linea a miExtractor1
with open ('allData.txt', encoding="utf8" ) as misDatos:
    for cadaLinea in misDatos:
        miExtractor1(cadaLinea)      
        
connnection.close()  
    
    