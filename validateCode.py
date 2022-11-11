
import barcodenumber

import barcodenumber

terminado=False

while not terminado:
    valorValidar = input("ingrese el codigo")
    if not barcodenumber.check_code('ean13',valorValidar):
        print("No válido")
        terminado = True
    else:
        print("valido")