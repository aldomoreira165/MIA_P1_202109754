from os import remove, path, makedirs

def crearDisco(nombre):
    try:
        # Creando las carpetas en caso no existan
        makedirs(path.dirname(nombre), exist_ok=True)

        # Creando el archivo en modo binario de escritura (modo "xb")
        fileOpen = open(nombre, "xb")
        print("Disco creado correctamente")
        return fileOpen
    except FileExistsError:
        print(f"El archivo '{nombre}' ya existe.")
    except Exception as e:
        print(f"Error creando disco: {e}")

def eliminarDisco(nombre):
    if path.exists(nombre):
        remove(nombre)
        print("Disco eliminado correctamente")
    else:
        print("Error: el archivo no se encuentra o no existe.")


def establecerEspacioDisco(archivo, espacio, unidad):
    buffer = b'\0' 
    if unidad == "k":
        bytes_per_unit = 1024  # 1KB en bytes
    elif unidad == "m":
        bytes_per_unit = 1024 * 1024  # 1MB en bytes
    else:
        print("Unidad de tamaño no válida")
        return

    times_to_write = espacio * bytes_per_unit

    for i in range(times_to_write):
        archivo.write(buffer)

    #print("Espacio establecido correctamente")


def generarDatosDisco(archivo, desplazamiento, objeto):
    try:
        #print("Escribiendo en: ", desplazamiento)
        datos = objeto.doSerialize()
        archivo.seek(desplazamiento)
        archivo.write(datos)
        print("escritura correcta")
    except Exception as e:
        print(f"Error en escritura disco: {e}")

def obtenerDatosDisco(nombre, desplazamiento,objeto):
    with open(nombre, "rb") as fileOpen:
        try:
            #print("Reading in: ", desplazamiento)
            #print("Size: ",  ctypes.sizeof(obj))
            fileOpen.seek(desplazamiento)
            data = fileOpen.read(len(objeto.doSerialize()))
            #print("Size data: ",  len(data))
            objeto.doDeserialize(data)
            print("lectura correcta")
        except Exception as e:
            print(f"Error reading object err: {e}")