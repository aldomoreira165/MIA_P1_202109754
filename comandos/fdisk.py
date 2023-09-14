import os
from elementos.superbloque import *
from elementos.inodo import *
from elementos.fileblock import *
from elementos.mbr import Mbr
from elementos.disco import *
from funciones.utilities import coding_str, decode_str
from elementos.ebr import Ebr

def execute_fdisk(args):
    if args.delete:
            nombre_particion = "b'" + args.name + "'"

            #buscar la particion y eliminarla
            if os.path.exists(args.path):
                mbrDisco = Mbr()

                #obteniendo datos del mbr
                obtenerDatosDisco(args.path, 0, mbrDisco)

                if str(mbrDisco.particion1.get_name()) == nombre_particion:
                    #preguntar si se desea eliminar la particion
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion1.eliminar()

                        with open(args.path, "rb+") as discoAbierto:
                            desocuparEspacio(discoAbierto, mbrDisco.particion1.start, mbrDisco.particion1.s)

                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion2.get_name()) == nombre_particion: 
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion2.eliminar()

                        with open(args.path, "rb+") as discoAbierto:
                            desocuparEspacio(discoAbierto, mbrDisco.particion2.start, mbrDisco.particion2.s)

                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion3.get_name()) == nombre_particion:
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion3.eliminar()

                        with open(args.path, "rb+") as discoAbierto:
                            desocuparEspacio(discoAbierto, mbrDisco.particion3.start, mbrDisco.particion3.s)

                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                elif str(mbrDisco.particion4.get_name()) == nombre_particion:
                    confirmacion = (input("Esta seguro que desea eliminar la particion? (S/N): ")).lower()
                    if confirmacion == "s":
                        mbrDisco.particion4.eliminar()

                        with open(args.path, "rb+") as discoAbierto:
                            desocuparEspacio(discoAbierto, mbrDisco.particion4.start, mbrDisco.particion4.s)

                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion eliminada exitosamente")
                    else:
                        print("Eliminacion de particion cancelada")
                else:
                    print("Error: particion no encontrada")

                mbrActualizado = Mbr()
                obtenerDatosDisco(args.path, 0, mbrActualizado)
                print("=====================particiones========================")
                mbrActualizado.particion1.display_info()
                print("*******************************************")
                mbrActualizado.particion2.display_info()
                print("*******************************************")
                mbrActualizado.particion3.display_info()
                print("*******************************************")
                mbrActualizado.particion4.display_info()
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
                espacio_ocupado = verificar_espacio_ocupado(args.path)
                condicion = espacio_ocupado + bytes_agregar
                if condicion <= mbrDisco.tamano and condicion > 0:
                    #buscar la particion a la que se la va a modificar el size
                    if str(mbrDisco.particion1.get_name()) == nombre_particion:
                        mbrDisco.particion1.set_s(int(mbrDisco.particion1.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion2.get_name()) == nombre_particion:
                        mbrDisco.particion2.set_s(int(mbrDisco.particion2.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion3.get_name()) == nombre_particion:
                        mbrDisco.particion3.set_s(int(mbrDisco.particion3.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion modificada exitosamente")
                    elif str(mbrDisco.particion4.get_name()) == nombre_particion:
                        mbrDisco.particion4.set_s(int(mbrDisco.particion4.s) + bytes_agregar)
                        actualizarParticionesMBR(args.path, mbrDisco)
                        actualizar_start_particiones(args.path)
                        print("particion modificada exitosamente")
                    else:
                        print("Error: particion no encontrada")

                    mbrActualizado = Mbr()
                    obtenerDatosDisco(args.path, 0, mbrActualizado)
                    print("=====================particiones========================")
                    mbrActualizado.particion1.display_info()
                    print("*******************************************")
                    mbrActualizado.particion2.display_info()
                    print("*******************************************")
                    mbrActualizado.particion3.display_info()
                    print("*******************************************")
                    mbrActualizado.particion4.display_info()
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
                    bytesSize = convertir_bytes(args.size, args.unit) 
                    espacio_ocupado = verificar_espacio_ocupado(args.path)
                    if espacio_ocupado + bytesSize <= mbrDisco.tamano:
                        if args.type != "l":
                            if mbrDisco.particion1.s == 0:
                                settearDatosParticion(mbrDisco, args.path, 1, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion2.s == 0:
                                settearDatosParticion(mbrDisco, args.path, 2, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion3.s == 0:
                                settearDatosParticion(mbrDisco, args.path, 3, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion4.s == 0:
                                settearDatosParticion(mbrDisco, args.path, 4, args.name, args.fit, args.type, args.unit, args.size)
                            else:
                                print("Ya no existen particiones libres")
                        else:
                            if mbrDisco.particion1.type == b'e':
                                settearDatosParticion(mbrDisco, args.path, 1, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion2.type == b'e':
                                settearDatosParticion(mbrDisco, args.path, 2, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion3.type == b'e':
                                settearDatosParticion(mbrDisco, args.path, 3, args.name, args.fit, args.type, args.unit, args.size)
                            elif mbrDisco.particion4.type == b'e':
                                settearDatosParticion(mbrDisco, args.path, 4, args.name, args.fit, args.type, args.unit, args.size)
                            else:
                                print("No existe una particion extendida")

                        mbrActualizado = Mbr()
                        obtenerDatosDisco(args.path, 0, mbrActualizado)
                        print("=====================particiones========================")
                        mbrActualizado.particion1.display_info()
                        print("*******************************************")
                        mbrActualizado.particion2.display_info()
                        print("*******************************************")
                        mbrActualizado.particion3.display_info()
                        print("*******************************************")
                        mbrActualizado.particion4.display_info()
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


def caseLogica(rutaDisco, fitParticion, sizeParticion, nombreParticion):
    puntero = -1
    inicio = -1
    size = -1
    ebrActual = Ebr()
    mbr = Mbr()
    obtenerDatosDisco(rutaDisco, 0, mbr)
    
    if mbr.particion1.type == b'e':
        inicio = mbr.particion1.start
        puntero = mbr.particion1.start
        size = mbr.particion1.s
    elif mbr.particion2.type == b'e':
            inicio = mbr.particion2.start
            puntero = mbr.particion2.start
            size = mbr.particion2.s
    elif mbr.particion3.type == b'e':
        inicio = mbr.particion3.start
        puntero = mbr.particion3.start
        size = mbr.particion3.s
    elif mbr.particion4.type == b'e':
        inicio = mbr.particion4.start
        puntero = mbr.particion4.start
        size = mbr.particion4.s

    #obteniendo el ebr
    while puntero < inicio + size:
        ebrActual = Ebr()
        obtenerDatosDisco(rutaDisco, puntero, ebrActual)
        if ebrActual.next == -1:
            break 
        else:  
            puntero += len(ebrActual.doSerialize()) + ebrActual.s

    #actualizando ebr
    part_start = ebrActual.start #numero de byte en el que inicia la particion
    part_next = part_start + sizeParticion #numero de byte en el que esta el proximo ebr
    ebrActual.set_infomation('0', fitParticion, part_start, sizeParticion, part_next, nombreParticion)
    
    with open(rutaDisco, "rb+") as discoAbierto:
        generarDatosDisco(discoAbierto, puntero, ebrActual)

    with open(rutaDisco, "rb+") as discoAbierto:
        rango = part_next - part_start
        ocuparEspacio(discoAbierto, part_start, rango)

    with open(rutaDisco, "rb+") as discoAbierto:
            #generar un mbr vacio en la posicion despues de la particion logica
            ebrUltimo = Ebr()
            startNext = part_next + len(ebrUltimo.doSerialize())
            ebrUltimo.set_infomation('0', '0', startNext, -1, -1, "noName")
            generarDatosDisco(discoAbierto, part_next, ebrUltimo)

#particiones extendidas
def caseExtendida(mbr, rutaDisco, numParticion):
    extendida = False
    inicio = -1
    size = 0

    if numParticion == 1:
        inicio = mbr.particion1.start
        size = mbr.particion1.s
        extendida = True
    elif numParticion == 2:
        inicio = mbr.particion2.start
        size = mbr.particion2.s
        extendida = True
    elif numParticion == 3:
        inicio = mbr.particion3.start
        size = mbr.particion3.s
        extendida = True
    elif numParticion == 4:
        inicio = mbr.particion4.start
        size = mbr.particion4.s
        extendida = True
    
    if extendida == True:
        setPrimerEBR(rutaDisco, inicio, size)      

def setPrimerEBR(rutaDisco, inicio, size):
    ebr = Ebr()
    part_start = inicio + len(ebr.doSerialize())
    ebr.set_infomation('0', '0', part_start, -1, -1, "noName")

    with open(rutaDisco, "rb+") as discoAbierto:
        generarDatosDisco(discoAbierto, inicio, ebr)

    with open(rutaDisco, "rb+") as discoAbierto:
        rango = size - len(ebr.doSerialize())
        inicioEspacio = inicio + len(ebr.doSerialize())
        ocuparEspacio(discoAbierto, inicioEspacio, rango)

def settearDatosParticion(mbr, path, numero_particion, name, fit, type, unit, size):
    nombres_particiones = [str(mbr.particion1.get_name()), str(mbr.particion2.get_name()), str(mbr.particion3.get_name()), str(mbr.particion4.get_name())]
    nombre_comparar = "b'" + name + "'"

    if numero_particion == 1:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            if set_tipo_particion(mbr, 1, type) == True:
                inicio = len(mbr.doSerialize())
                mbr.particion1.set_name(name)
                mbr.particion1.set_fit(fit)
                mbr.particion1.set_start(inicio)
                bytesConv = 0

                if unit == "b":
                    mbr.particion1.set_s(size)
                    bytesConv = size
                elif unit== "k":
                    size_k = size * 1024
                    bytesConv = size_k
                    mbr.particion1.set_s(size_k)
                elif unit == "m":
                    size_w = size * 1024 * 1024
                    bytesConv = size_w
                    mbr.particion1.set_s(size_w)
                else:
                    print("unidad de particion incorrecta")

                if mbr.particion1.type != b'l':
                    actualizarParticionesMBR(path, mbr)
                    actualizar_start_particiones(path)

                    with open(path, "rb+") as discoAbierto:
                        ocuparEspacio(discoAbierto, inicio, mbr.particion1.s)

                    if mbr.particion1.type == b'e':
                        caseExtendida(mbr, path, 1)
                else:
                    caseLogica(path, fit, bytesConv, name)

    elif numero_particion == 2:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            if set_tipo_particion(mbr, 2, type) == True:
                inicio = len(mbr.doSerialize()) + mbr.particion1.s
                mbr.particion2.set_name(name)
                mbr.particion2.set_fit(fit)
                mbr.particion2.set_start(inicio)
                bytesConv = 0

                if unit == "b":
                    mbr.particion2.set_s(size)
                    bytesConv = size
                elif unit== "k":
                    size_k = size * 1024
                    bytesConv = size_k
                    mbr.particion2.set_s(size_k)
                elif unit == "m":
                    size_w = size * 1024 * 1024
                    bytesConv = size_w
                    mbr.particion2.set_s(size_w)
                else:
                    print("unidad de particion incorrecta")
                if mbr.particion2.type != b'l':
                    actualizarParticionesMBR(path, mbr)
                    actualizar_start_particiones(path)
                    
                    if mbr.particion2.type == b'p':
                        with open(path, "rb+") as discoAbierto:
                            ocuparEspacio(discoAbierto, inicio, mbr.particion2.s)

                    if mbr.particion2.type == b'e':
                        caseExtendida(mbr, path, 2)
                else:
                    caseLogica(path, fit, bytesConv, name)
                
    elif numero_particion == 3:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            if set_tipo_particion(mbr, 3, type) == True:
                inicio = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s
                mbr.particion3.set_name(name)
                mbr.particion3.set_fit(fit)
                mbr.particion3.set_start(inicio)
                bytesConv = 0

                if unit == "b":
                    mbr.particion3.set_s(size)
                    bytesConv = size
                elif unit== "k":
                    size_k = size * 1024
                    bytesConv = size_k
                    mbr.particion3.set_s(size_k)
                elif unit == "m":
                    size_w = size * 1024 * 1024
                    bytesConv = size_w
                    mbr.particion3.set_s(size_w)
                else:
                    print("unidad de particion incorrecta")
                if mbr.particion3.type != b'l':
                    actualizarParticionesMBR(path, mbr)
                    actualizar_start_particiones(path)
                    
                    if mbr.particion3.type == b'p':
                        with open(path, "rb+") as discoAbierto:
                            ocuparEspacio(discoAbierto, inicio, mbr.particion3.s)

                    if mbr.particion3.type == b'e':
                        caseExtendida(mbr, path, 3)
                else:
                    caseLogica(path, fit, bytesConv, name)

    elif numero_particion == 4:
        if nombre_comparar in nombres_particiones:
            print("Error: nombre de particion ya existe")
        else:
            if set_tipo_particion(mbr, 4, type) == True:
                inicio = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s
                mbr.particion4.set_name(name)
                mbr.particion4.set_fit(fit)
                mbr.particion4.set_start(inicio)
                bytesConv = 0

                if unit == "b":
                    mbr.particion4.set_s(size)
                    bytesConv = size
                elif unit== "k":
                    size_k = size * 1024
                    bytesConv = size_k
                    mbr.particion4.set_s(size_k)
                elif unit == "m":
                    size_w = size * 1024 * 1024
                    bytesConv = size_w
                    mbr.particion4.set_s(size_w)
                else:
                    print("unidad de particion incorrecta")
                if mbr.particion4.type != b'l':
                    actualizarParticionesMBR(path, mbr)
                    actualizar_start_particiones(path)
                    ocuparEspacio(path, inicio, inicio + mbr.particion4.s)

                    if mbr.particion4.type == b'p':
                        with open(path, "rb+") as discoAbierto:
                            ocuparEspacio(discoAbierto, inicio, mbr.particion4.s)

                    if mbr.particion4.type == b'e':
                        caseExtendida(mbr, path, 4)
                else:
                    caseLogica(path, fit, bytesConv, name)
    
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
            print("Error: no existe una particion extendida")
            return False
        else:
            #aca es posible realizar las validaciones de las particiones logicas
            if numero_particion == 1:
                mbr.particion1.set_type(type)
            elif numero_particion == 2:
                mbr.particion2.set_type(type)
            elif numero_particion == 3:
                mbr.particion3.set_type(type)
            elif numero_particion == 4:
                mbr.particion4.set_type(type)
            return True
        
#funcion para verificar si ya existe particion extendida
def verificar_particion_extendida(mbr):
    if mbr.particion1.type == b'e' or mbr.particion2.type == b'e' or mbr.particion3.type == b'e' or mbr.particion4.type == b'e':
        return True
    else:
        return False

#funcion para verificar si existe espacio en el disco
def verificar_espacio_ocupado(disco):
    mbr = Mbr()
    obtenerDatosDisco(disco, 0, mbr)
    espacio_ocupado = len(mbr.doSerialize()) + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s + mbr.particion4.s
    return espacio_ocupado

#funcion para actualizar el mbr
def actualizarParticionesMBR(rutaDisco, mbr):
    disco = open(rutaDisco, "rb+")
    generarDatosDisco(disco, 0, mbr)
    disco.close()

#funcion para actualizar la posicion de donde inicia una particion
def actualizar_start_particiones(rutaDisco):
    mbr = Mbr()
    obtenerDatosDisco(rutaDisco, 0, mbr)
    mbr_espacio = len(mbr.doSerialize())

    if mbr.particion1.s > 0:
        mbr.particion1.set_start(mbr_espacio)

    if mbr.particion2.s > 0:
        mbr.particion2.set_start(mbr_espacio + mbr.particion1.s)

    if mbr.particion3.s > 0:
        mbr.particion3.set_start(mbr_espacio + mbr.particion1.s + mbr.particion2.s)
    
    if mbr.particion4.s > 0:
        mbr.particion4.set_start(mbr_espacio + mbr.particion1.s + mbr.particion2.s + mbr.particion3.s)

    actualizarParticionesMBR(rutaDisco, mbr)

def convertir_bytes(size, unit):
    if unit == "b":
        bytes = size
    elif unit == "k":
        bytes = size * 1024
    elif unit == "m":
        bytes= size * 1024 * 1024

    return bytes