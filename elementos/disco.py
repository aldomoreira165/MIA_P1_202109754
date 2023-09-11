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


def generarDatosDisco(archivo, desplazamiento, objeto):
    try:
        #print("Escribiendo en: ", desplazamiento)
        datos = objeto.doSerialize()
        archivo.seek(desplazamiento)
        archivo.write(datos)
    except Exception as e:
        print(f"Error en escritura disco: {e}")

def obtenerDatosDisco(nombre, desplazamiento,objeto):
    with open(nombre, "rb") as fileOpen:
        try:
            fileOpen.seek(desplazamiento)
            data = fileOpen.read(len(objeto.doSerialize()))
            objeto.doDeserialize(data)
        except Exception as e:
            print(f"Error reading object err: {e}")

def obtener_total_bytes(size, unit):
    if unit == "k":
        return size * 1024
    elif unit == "m":
        return size * 1024 * 1024
    else:
        return "Error de unidad"
    

def ocuparEspacio(disco, desplazamiento, rango):
    try:
        disco.seek(desplazamiento)
        uno = b'1'
        for i in range(rango):
            disco.write(uno)
    except Exception as e:
        print(f"Error en cambio disco: {e}")

def desocuparEspacio(disco, desplazamiento, rango):
    try:
        disco.seek(desplazamiento)
        cero = b'\0'
        for i in range(rango):
            disco.write(cero)
    except Exception as e:
        print(f"Error en cambio disco: {e}")