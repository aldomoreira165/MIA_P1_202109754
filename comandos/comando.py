import os
import struct
import math
import datetime
from elementos.superbloque import *
from elementos.inodo import *
from elementos.bloque_archivos import *
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
            bytes = obtener_total_bytes(args.size, args.unit)
            date = coding_str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 16)
            mbr.set_infomation(bytes, date, args.fit)

            #generando objeto mbr en el disco
            generarDatosDisco(discoCreado, 0, mbr)
            
            discoCreado.close()

            #leer 
            mbrDEs = Mbr()
            obtenerDatosDisco(args.path, 0, mbrDEs)
            mbrDEs.display_info()
            
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
                        elif mbrDisco.particion2.s == 0:
                            settearDatosParticion(mbrDisco, 2, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        elif mbrDisco.particion3.s == 0:
                            settearDatosParticion(mbrDisco, 3, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        elif mbrDisco.particion4.s == 0:
                            settearDatosParticion(mbrDisco, 4, args.name, args.fit, args.type, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        else:
                            print("Ya no existen particiones libres")

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
                        espacio_libre = mbrDisco.tamano - espacio_ocupado
                        print("Error: no hay espacio suficiente en el disco. Espacio libre: ", espacio_libre)
                else:
                    print("Error: El disco no existe.")
            else:
                print("Error: El tamaño de la particion debe ser positivo y mayor que 0.")
        else:
            print("Error: El tamaño de la particion (-size) es obligatorio.")
        
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
                set_tipo_particion(mbr, numero_particion, type)

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
                size_particion = mbrDisco.particion1.s
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
                size_particion = mbrDisco.particion2.s
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
                size_particion = mbrDisco.particion3.s
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
                size_particion = mbrDisco.particion4.s
                particion_a_montar = [id_particion, mbrDisco.particion4, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        else:
            print("Error: particion no encontrada")

    else:
        print("Error: El disco no existe.")

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

def execute_mkfs(args):
    particion_montada = None
    for particion in particiones_montadas:
        if particion[0] == args.id:
            particion_montada = particion
            break

    if particion_montada == None:
        print("Error: particion no montada")
    else:
        numerador = particion_montada[1].s - struct.calcsize(Superblock().getConst())
        denominador = 4 + struct.calcsize(Inode().getConst()) + 3 * struct.calcsize(Fileblock().getConst())
        temp = 0 if args.fs == 2 else 0
        n = math.floor(numerador / denominador)

        #creando superbloque
        new_superblock = Superblock()
        new_superblock.inodes_count = 0
        new_superblock.blocks_count = 0
        new_superblock.free_blocks_count = 3 * n
        new_superblock.free_inodes_count = n
        date = coding_str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 16)
        new_superblock.mtime = date
        new_superblock.umtime = date
        new_superblock.mcount = 1

        if args.fs == "2fs":
            create_ext2(n, particion_montada, new_superblock, date)
        elif args.fs == 3:
            pass


def create_ext2(n, mPartition, new_superblock, date):
    new_superblock.filesystem_type = 2
    new_superblock.bm_inode_start = mPartition[1].start + struct.calcsize(Superblock().getConst())
    new_superblock.bm_block_start = new_superblock.bm_inode_start + n
    new_superblock.inode_start = new_superblock.bm_block_start +    3 * n
    new_superblock.block_start = new_superblock.inode_start + n * struct.calcsize(Inode().getConst())

    new_superblock.free_inodes_count -= 1
    new_superblock.free_blocks_count -= 1
    new_superblock.free_inodes_count -= 1
    new_superblock.free_blocks_count -= 1

    Crr_file = open(mPartition[2], "rb+")
    generarDatosDisco(Crr_file, mPartition[1].start, new_superblock)

    zero = '0'

    for i in range(n):
        generarDatosDisco(Crr_file, new_superblock.bm_inode_start + i, zero)

    for i in range(3 * n):
        generarDatosDisco(Crr_file, new_superblock.bm_block_start + i, zero)

    new_inode = Inode()
    for i in range(n): 
        generarDatosDisco(Crr_file, new_superblock.inode_start + i * struct.calcsize(Inode().getConst()), new_inode)

    new_Fileblock = Fileblock()
    for i in range(3 * n):
        generarDatosDisco(Crr_file, new_superblock.block_start + i * struct.calcsize(Fileblock().getConst()), new_Fileblock)

    Crr_file.close()
    print("Sistema de archivos creado exitosamente")
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

#python main.py execute -path=./hola.txt