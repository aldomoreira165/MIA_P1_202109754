import os
from elementos.mbr import Mbr
from elementos.disco import *
from funciones.utilities import coding_str

particiones_montadas = []

def execute_mkdisk(args):
    if args.size > 0:

        try:
            #creando disco
            discoCreado = crearDisco(args.path)

            #creando espacio de disco
            establecerEspacioDisco(discoCreado, args.size, args.unit)

            #creando mbr de disco
            mbr = Mbr()
            mbr.set_infomation(args.size, args.fit)

            #generando objeto mbr en el disco
            generarDatosDisco(discoCreado, 0, mbr)
            
            discoCreado.close()

            #leer 
            mbrDEs = Mbr()
            obtenerDatosDisco(args.path, 0, mbrDEs)
            mbrDEs.display_info()

            """
            print("====particiones======")
            print("----particion 1 -----")
            mbrDEs.particion1.set_status("A")
            mbrDEs.particion1.display_info()
            print("----particion 2 -----")
            mbrDEs.particion2.display_info()
            print("----particion 3 -----")
            mbrDEs.particion3.display_info()
            print("----particion 4 -----")
            mbrDEs.particion4.display_info()"""
            
        except Exception as e:
            print(f"Error configurando disco: {e}")
    else:
        print("Error: El tamaño del disco debe ser positivo y mayor que 0.")
        
def execute_rmdisk(args):   
    confirmacion = (input("Esta seguro que desea eliminar el disco? (S/N): ")).lower()
    if confirmacion == "s":
        eliminarDisco(args.path)
    else:
        print("Eliminacion de disco cancelada") 


def execute_fdisk(args):
    if args.size > 0:
        if os.path.exists(args.path):
            mbrDisco = Mbr()

            print("==========================antes==========================")
            mbrDisco.particion1.display_info()
            print("*******************************************")
            mbrDisco.particion2.display_info()
            print("*******************************************")
            mbrDisco.particion3.display_info()
            print("*******************************************")
            mbrDisco.particion4.display_info()
            print("*******************************************")

            #obteniendo datos del mbr
            obtenerDatosDisco(args.path, 0, mbrDisco)

            if mbrDisco.particion1.s == 0:
                settearDatosParticion(mbrDisco, 1, args.name, args.fit, args.unit, args.size)
                actualizarParticionesMBR(args.path, mbrDisco)
            elif mbrDisco.particion2.s == 0:
                settearDatosParticion(mbrDisco, 2, args.name, args.fit, args.unit, args.size)
                actualizarParticionesMBR(args.path, mbrDisco)
            elif mbrDisco.particion3.s == 0:
                settearDatosParticion(mbrDisco, 3, args.name, args.fit, args.unit, args.size)
                actualizarParticionesMBR(args.path, mbrDisco)
            elif mbrDisco.particion4.s == 0:
                settearDatosParticion(mbrDisco, 4, args.name, args.fit, args.unit, args.size)
                actualizarParticionesMBR(args.path, mbrDisco)
            else:
                print("Ya no existen particiones libres")

            print("=====================despues========================")
            mbrDisco.particion1.display_info()
            print("*******************************************")
            mbrDisco.particion2.display_info()
            print("*******************************************")
            mbrDisco.particion3.display_info()
            print("*******************************************")
            mbrDisco.particion4.display_info()
            print("*******************************************")

        else:
            print("Error: El disco no existe.")
    else:
        print("Error: El tamaño de la particion debe ser positivo y mayor que 0.")
        
def settearDatosParticion(mbr, numero_particion, name, fit, unit, size):
    nombres_particiones = [str(mbr.particion1.get_name()), str(mbr.particion2.get_name()), str(mbr.particion3.get_name()), str(mbr.particion4.get_name())]
    nombre_comparar = "b'" + name + "'"

    if numero_particion == 1:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            inicio = len(mbr.doSerialize())
            mbr.particion1.set_name(name)
            mbr.particion1.set_fit(fit)
            mbr.particion1.set_start(inicio)

            if unit == "b":
                mbr.particion1.set_s(size)
            elif unit== "k":
                size_k = size * 1024
                mbr.particion1.set_s(size_k)
            elif unit == "m":
                size_w = size * 1024 * 1024
                mbr.particion1.set_s(size_w)
            else:
                print("unidad de particion incorrecta")

    elif numero_particion == 2:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            inicio = len(mbr.doSerialize()) + mbr.particion1.s
            mbr.particion2.set_name(name)
            mbr.particion2.set_fit(fit)
            mbr.particion2.set_start(inicio)

            if unit == "b":
                mbr.particion2.set_s(size)
            elif unit== "k":
                size_k = size * 1024
                mbr.particion2.set_s(size_k)
            elif unit == "m":
                size_w = size * 1024 * 1024
                mbr.particion2.set_s(size_w)
            else:
                print("unidad de particion incorrecta")

    elif numero_particion == 3:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            inicio = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s
            mbr.particion3.set_name(name)
            mbr.particion3.set_fit(fit)
            mbr.particion3.set_start(inicio)

            if unit == "b":
                mbr.particion3.set_s(size)
            elif unit== "k":
                size_k = size * 1024
                mbr.particion3.set_s(size_k)
            elif unit == "m":
                size_w = size * 1024 * 1024
                mbr.particion3.set_s(size_w)
            else:
                print("unidad de particion incorrecta")

    elif numero_particion == 4:

        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            inicio = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s
            mbr.particion4.set_name(name)
            mbr.particion4.set_fit(fit)
            mbr.particion4.set_start(inicio)

            if unit == "b":
                mbr.particion4.set_s(size)
            elif unit== "k":
                size_k = size * 1024
                mbr.particion4.set_s(size_k)
            elif unit == "m":
                size_w = size * 1024 * 1024
                mbr.particion4.set_s(size_w)
            else:
                print("unidad de particion incorrecta")

def actualizarParticionesMBR(rutaDisco, mbr):
    disco = open(rutaDisco, "rb+")
    generarDatosDisco(disco, 0, mbr)
    disco.close()

def execute_mount(args):
    if os.path.exists(args.path):
        mbrDisco = Mbr()

        #obteniendo datos del mbr
        obtenerDatosDisco(args.path, 0, mbrDisco)

        digitos_carnet = "54"
        nombre_disco = os.path.splitext(os.path.basename(args.path))[0]
        nombre_buscar = "b'" + args.name + "'"

        #buscar la particion a cargar en base al nombre
        if str(mbrDisco.particion1.get_name()) == nombre_buscar:
            numero_particion = "1"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particiones_montadas.append(id_particion)
                print("Particion montada correctamente")
                print("Pariciones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion2.get_name()) == nombre_buscar: 
            numero_particion = "2"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particiones_montadas.append(id_particion)
                print("Particion montada correctamente")
                print("Pariciones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion3.get_name()) == nombre_buscar:
            numero_particion = "3"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particiones_montadas.append(id_particion)
                print("Particion montada correctamente")
                print("Pariciones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion4.get_name()) == nombre_buscar:
            numero_particion = "4"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particiones_montadas.append(id_particion)
                print("Particion montada correctamente")
                print("Pariciones montadas: ", particiones_montadas)
        else:
            print("Error: particion no encontrada")

    else:
        print("Error: El disco no existe.")

def execute_unmount(args):
    id = args.id

    if id in particiones_montadas:
        particiones_montadas.remove(id)
        print("Particion desmontada correctamente")
        print("Pariciones montadas: ", particiones_montadas)
    else:
        print("Error: particion no montada")


#python main.py execute -path=./hola.txt