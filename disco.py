from os import remove, path, makedirs

def crearDisco(nombre):
    try:
        #creando las carpetas en caso no existan
        makedirs(path.dirname(nombre), exist_ok=True)

        #creando el archivo en modo binario de escritura
        fileOpen = open(nombre, "wb")  # Open the file in write mode
        print("Disco creado correctamente")
        return fileOpen
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
    if unidad == "K":
        bytes_per_unit = 1024  # 1KB en bytes
    elif unidad == "M":
        bytes_per_unit = 1024 * 1024  # 1MB en bytes
    else:
        print("Unidad de tamaño no válida")
        return

    times_to_write = espacio * bytes_per_unit

    for i in range(times_to_write):
        archivo.write(buffer)

    print("Espacio establecido correctamente")


def escribirDisco(archivo, desplazamiento, objeto):
    print("Escribiendo en: ", desplazamiento)
    datos = objeto.doSerialize()
    archivo.seek(desplazamiento)
    archivo.write(datos)