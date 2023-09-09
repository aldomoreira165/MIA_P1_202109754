import os
from elementos.superbloque import *
from elementos.inodo import *
from elementos.bloque_archivos import *
from elementos.mbr import Mbr
from elementos.disco import *
from funciones.utilities import coding_str, decode_str
from elementos.ebr import Ebr

def execute_fdisk(args):
    if args.delete:
            nombre_particion = "b'" + args.name + "'"
            path = args.path

            #buscar la particion y eliminarla
            if os.path.exists(path):
                mbrDisco = Mbr()

                #obteniendo datos del mbr
                obtenerDatosDisco(path, 0, mbrDisco)

                if str(mbrDisco.particion1.get_name()) == nombre_particion:
                    #preguntar si se desea eliminar la particion
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion1.eliminar()
                        actualizarParticionesMBR(path, mbrDisco)
                        actualizar_start_particiones(path, mbrDisco)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion2.get_name()) == nombre_particion: 
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion2.eliminar()
                        actualizarParticionesMBR(path, mbrDisco)
                        actualizar_start_particiones(path, mbrDisco)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion3.get_name()) == nombre_particion:
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion3.eliminar()
                        actualizarParticionesMBR(path, mbrDisco)
                        actualizar_start_particiones(path, mbrDisco)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion4.get_name()) == nombre_particion:
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion4.eliminar()
                        actualizarParticionesMBR(path, mbrDisco)
                        actualizar_start_particiones(path, mbrDisco)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                else:
                    print("Error: particion no encontrada")

                print("=====================particiones========================")
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
    elif args.add:
        if args.unit:
            if os.path.exists(args.path):
                mbrDisco = Mbr()
                obtenerDatosDisco(args.path, 0, mbrDisco)

                bytes = 0
                nombre_particion = "b'" + args.name + "'"

                if args.unit == "b":
                    bytes = args.add
                elif args.unit == "k":
                    bytes = args.add * 1024
                elif args.unit == "m":
                    bytes= args.add * 1024 * 1024

                bytes_agregar = int(bytes)
                
                #verificar si no sobrepasa el tamaño del disco
                espacio_ocupado = verificar_espacio_disco(args.path)
                if espacio_ocupado + bytes_agregar <= mbrDisco.tamano:
                    #buscar la particion a la que se la va a modificar el size
                    if str(mbrDisco.particion1.get_name()) == nombre_particion:
                        inicio = len(mbrDisco.doSerialize())
                        mbrDisco.particion1.set_s(int(mbrDisco.particion1.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path, mbrDisco)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion2.get_name()) == nombre_particion:
                        inicio = len(mbrDisco.doSerialize()) + mbrDisco.particion1.s
                        mbrDisco.particion2.set_s(int(mbrDisco.particion2.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path, mbrDisco)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion3.get_name()) == nombre_particion:
                        inicio = len(mbrDisco.doSerialize()) + mbrDisco.particion1.s + mbrDisco.particion2.s
                        mbrDisco.particion3.set_s(int(mbrDisco.particion3.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path, mbrDisco)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion4.get_name()) == nombre_particion:
                        inicio = len(mbrDisco.doSerialize()) + mbrDisco.particion1.s + mbrDisco.particion2.s + mbrDisco.particion3.s
                        mbrDisco.particion4.set_s(int(mbrDisco.particion4.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path, mbrDisco)
                        print("particion modificada exitosamente")
                    else:
                        print("Error: particion no encontrada")

                    print("=====================particiones========================")
                    mbrDisco.particion1.display_info()
                    print("*******************************************")
                    mbrDisco.particion2.display_info()
                    print("*******************************************")
                    mbrDisco.particion3.display_info()
                    print("*******************************************")
                    mbrDisco.particion4.display_info()
                    print("*******************************************")
                else:
                    print("Error: no hay espacio suficiente en el disco")
            else:
                print("Error: El disco no existe.")   
        else:
            print("Error: El parametro (-unit) es obligatorio")
    else:
        if args.size:
            if args.size > 0:
                if os.path.exists(args.path):
                    mbrDisco = Mbr()
                    #obteniendo datos del mbr
                    obtenerDatosDisco(args.path, 0, mbrDisco)

                    #verificar si hay espacio en el disco
                    espacio_ocupado = verificar_espacio_disco(args.path)
                    if espacio_ocupado + args.size <= mbrDisco.tamano:
                        if mbrDisco.particion1.s == 0:
                            settearDatosParticion(mbrDisco, 1, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                            caseExtendida(mbrDisco, args.path, 1)
                        elif mbrDisco.particion2.s == 0:
                            settearDatosParticion(mbrDisco, 2, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                            caseExtendida(mbrDisco, args.path, 2)
                        elif mbrDisco.particion3.s == 0:
                            settearDatosParticion(mbrDisco, 3, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                            caseExtendida(mbrDisco, args.path, 3)
                        elif mbrDisco.particion4.s == 0:
                            settearDatosParticion(mbrDisco, 4, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                            caseExtendida(mbrDisco, args.path, 4)
                        else:
                            print("Ya no existen particiones libres")

                        print("=====================particiones========================")
                        mbrDisco.particion1.display_info()
                        if mbrDisco.particion1.type == b'e':
                            print("--extendida--")
                            ebr = Ebr()
                            obtenerDatosDisco(args.path, mbrDisco.particion1.start, ebr)
                            ebr.display_info()
                        print("*******************************************")
                        mbrDisco.particion2.display_info()
                        if mbrDisco.particion2.type == b'e':
                            print("--extendida--")
                            ebr = Ebr()
                            obtenerDatosDisco(args.path, mbrDisco.particion2.start, ebr)
                            ebr.display_info()
                        print("*******************************************")
                        mbrDisco.particion3.display_info()
                        if mbrDisco.particion3.type == b'e':
                            print("--extendida--")
                            ebr = Ebr()
                            obtenerDatosDisco(args.path, mbrDisco.particion3.start, ebr)
                            ebr.display_info()
                        print("*******************************************")
                        mbrDisco.particion4.display_info()
                        if mbrDisco.particion4.type == b'e':
                            print("--extendida--")
                            ebr = Ebr()
                            obtenerDatosDisco(args.path, mbrDisco.particion4.start, ebr)
                            ebr.display_info()
                        print("*******************************************")
                    else:
                        espacio_libre = mbrDisco.tamano - espacio_ocupado
                        print("Error: no hay espacio suficiente en el disco. Espacio libre: ", espacio_libre)
                else:
                    print("Error: El disco no existe.")
            else:
                print("Error: El tamaño de la particion debe ser positivo y mayor que 0.")
        else:
            print("Error: El tamaño de la particion (-size) es obligatorio.")

def caseExtendida(mbr, disco, numParticion):
    extendida = False
    inicio = -1
    size = 0
    name = ""

    if numParticion == 1:
        if mbr.particion1.type == b'e':
            inicio = mbr.particion1.start
            size = mbr.particion1.s
            name = mbr.particion1.get_name()
            extendida = True
 
            if extendida:
                with open(disco, "rb+") as discoAbierto:
                    setDataEBR(discoAbierto, inicio, size, name)

    elif numParticion == 2:
        if mbr.particion2.type == b'e':
            inicio = mbr.particion2.start
            size = mbr.particion2.s
            name = mbr.particion2.get_name()
            extendida = True
            
            if extendida:
                with open(disco, "rb+") as discoAbierto:
                    setDataEBR(discoAbierto, inicio, size, name)

    elif numParticion == 3:
        if mbr.particion3.type == b'e':
            inicio = mbr.particion3.start
            size = mbr.particion3.s
            name = mbr.particion3.get_name()
            extendida = True
            
            if extendida:
                with open(disco, "rb+") as discoAbierto:
                    setDataEBR(discoAbierto, inicio, size, name)
    elif numParticion == 4:
        if mbr.particion4.type == b'e':
            inicio = mbr.particion4.start
            size = mbr.particion4.s
            name = mbr.particion4.get_name()
            extendida = True

            if extendida:
                with open(disco, "rb+") as discoAbierto:
                    setDataEBR(discoAbierto, inicio, size, name)      

def setDataEBR(discoAbierto, inicio, size, name):
    ebr = Ebr()
    nameString = decode_str(name)
    ebr.set_infomation('0', '0', inicio, size, -1, nameString)
    generarDatosDisco(discoAbierto, inicio, ebr)

def settearDatosParticion(mbr, numero_particion, name, fit, type, unit, size):
    nombres_particiones = [str(mbr.particion1.get_name()), str(mbr.particion2.get_name()), str(mbr.particion3.get_name()), str(mbr.particion4.get_name())]
    nombre_comparar = "b'" + name + "'"

    if numero_particion == 1:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            if set_tipo_particion(mbr, numero_particion, type) == True:
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
            if set_tipo_particion(mbr, numero_particion, type) == True:
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
            if set_tipo_particion(mbr, numero_particion, type) == True:
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
            if set_tipo_particion(mbr, numero_particion, type) == True:
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

#funcion para verificar si ya existe particion extendida
def verificar_particion_extendida(mbr):
    if mbr.particion1.type == b'e' or mbr.particion2.type == b'e' or mbr.particion3.type == b'e' or mbr.particion4.type == b'e':
        return True
    else:
        return False
    
#funcion para setter tipo de particion
def set_tipo_particion(mbr, numero_particion, type):

    if type == "e":
        if verificar_particion_extendida(mbr)  == True:
            print("Error: ya existe una particion extendida")
            return False
        else:
            if numero_particion == 1:
                mbr.particion1.set_type(type)
            elif numero_particion == 2:
                mbr.particion2.set_type(type)
            elif numero_particion == 3:
                mbr.particion3.set_type(type)
            elif numero_particion == 4:
                mbr.particion4.set_type(type)
            return True
    elif type == "p":
        if numero_particion == 1:
            mbr.particion1.set_type(type)
        elif numero_particion == 2:
            mbr.particion2.set_type(type)
        elif numero_particion == 3:
            mbr.particion3.set_type(type)
        elif numero_particion == 4:
            mbr.particion4.set_type(type)
        return True
    elif type == "l":
        if verificar_particion_extendida(mbr) == False:
            print("Error: no existe particion extendida")
            return False
        else:
            
            print("Creando particion logica")
            return True

#funcion para verificar si existe espacio en el disco
def verificar_espacio_disco(disco):
    mbr = Mbr()
    obtenerDatosDisco(disco, 0, mbr)
    espacio_ocupado = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s + mbr.particion4.s
    return espacio_ocupado

#funcion para actualizar el mbr
def actualizarParticionesMBR(rutaDisco, mbr):
    disco = open(rutaDisco, "rb+")
    generarDatosDisco(disco, 0, mbr)
    disco.close()

#funcion para actualizar el start al agregar o eliminar una particion
def actualizar_start_particiones(disco, mbr):
    mbr_espacio = len(mbr.doSerialize())
    obtenerDatosDisco(disco, 0, mbr)

    if mbr.particion1.s > 0:
        mbr.particion1.set_start(mbr_espacio)

    if mbr.particion2.s > 0:
        mbr.particion2.set_start(mbr_espacio + mbr.particion1.s)

    if mbr.particion3.s > 0:
        mbr.particion3.set_start(mbr_espacio + mbr.particion1.s + mbr.particion2.s)
    
    if mbr.particion4.s > 0:
        mbr.particion4.set_start(mbr_espacio + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s)

    actualizarParticionesMBR(disco, mbr)