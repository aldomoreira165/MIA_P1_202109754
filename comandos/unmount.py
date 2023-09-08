import os
from elementos.disco import *
from elementos.mbr import Mbr
from comandos.mount import particiones_montadas

def execute_unmount(args):
    id = args.id
    elemento_encontrado = None

    for elemento in particiones_montadas:
        if elemento[0] == id:
            elemento_encontrado = elemento
            break

    if elemento_encontrado:
        particiones_montadas.remove(elemento_encontrado)
        print("Particion desmontada correctamente")
        print("Particiones montadas: ", particiones_montadas)
    else:
        print("Error: particion no encontrada")