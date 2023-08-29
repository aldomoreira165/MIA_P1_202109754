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
            bytes = obtener_total_bytes(args.size, args.unit)
            mbr.set_infomation(bytes, args.fit)

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
                            settearDatosParticion(mbrDisco, 1, args.name, args.fit, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        elif mbrDisco.particion2.s == 0:
                            settearDatosParticion(mbrDisco, 2, args.name, args.fit, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        elif mbrDisco.particion3.s == 0:
                            settearDatosParticion(mbrDisco, 3, args.name, args.fit, args.unit, args.size)
                            actualizarParticionesMBR(args.path, mbrDisco)
                            actualizar_start_particiones(args.path, mbrDisco)
                        elif mbrDisco.particion4.s == 0:
                            settearDatosParticion(mbrDisco, 4, args.name, args.fit, args.unit, args.size)
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
                particion_a_montar = [id_particion, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion2.get_name()) == nombre_buscar: 
            numero_particion = "2"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion3.get_name()) == nombre_buscar:
            numero_particion = "3"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, args.path]
                particiones_montadas.append(particion_a_montar)
                print("Particion montada correctamente")
                print("Particiones montadas: ", particiones_montadas)
        elif str(mbrDisco.particion4.get_name()) == nombre_buscar:
            numero_particion = "4"
            id_particion = digitos_carnet + numero_particion + nombre_disco
            if id_particion in particiones_montadas:
                print("Error: particion ya montada")
            else:
                particion_a_montar = [id_particion, args.path]
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