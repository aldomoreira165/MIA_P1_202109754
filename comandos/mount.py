import os
from elementos.superbloque import *
from elementos.inodo import *
from elementos.fileblock import *
from elementos.mbr import Mbr
from elementos.disco import *

particiones_montadas = []

def execute_mount(args):
    if os.path.exists(args.path):
        mbrDisco = Mbr()
        montada = False

        #obteniendo datos del mbr
        obtenerDatosDisco(args.path, 0, mbrDisco)

        digitos_carnet = "54"
        nombre_disco = os.path.splitext(os.path.basename(args.path))[0]
        nombre_buscar = "b'" + args.name + "'"

        #buscar la particion a cargar en base al nombre
        if str(mbrDisco.particion1.get_name()) == nombre_buscar:
            numero_particion = "1"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            
            #recorrer particiones montadas para verificar que no este montada
            for particion in particiones_montadas:
                if particion[0] == id_particion:
                    montada = True
                    break
                
            if montada == True:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, mbrDisco.particion1, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion2.get_name()) == nombre_buscar: 
            numero_particion = "2"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, mbrDisco.particion2, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion3.get_name()) == nombre_buscar:
            numero_particion = "3"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, mbrDisco.particion3, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion4.get_name()) == nombre_buscar:
            numero_particion = "4"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, mbrDisco.particion4, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        else:
            print("Error: particion no encontrada")

    else:
        print("Error: El disco no existe.")

